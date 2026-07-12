"""Two-stage retrieval: whole-file selection -> AST split -> chunk retrieval."""

from __future__ import annotations

import pytest

from gitflame_coderag.chunking.document import build_document_chunks, chunk_file_as_document
from gitflame_coderag.pipelines.two_stage_retrieve import (
    DocumentExpander,
    apply_document_prior,
    build_document_index,
    make_document_expander,
    run_two_stage_retrieval,
    select_documents,
)
from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ChunkingConfig,
    CodeChunk,
    DocumentCandidate,
    ExperimentConfig,
    FileMetadata,
    Issue,
    RepositoryFile,
    RetrievalResult,
    StructuralMetadata,
)

BILLING_FILE = '''
import decimal


class InvoiceCalculator:
    """Compute invoice totals."""

    def apply_discount(self, total, discount_rate):
        return total * (1 - discount_rate)

    def compute_total(self, items):
        return sum(item.price for item in items)


def render_invoice_pdf(invoice):
    return f"pdf:{invoice.id}"
'''

AUTH_FILE = '''
def login(username, password):
    return username == password


def logout(session):
    session.clear()
'''


def make_file(path: str, content: str) -> RepositoryFile:
    return RepositoryFile(
        metadata=FileMetadata(
            id=f"repo:rev:{path}",
            repository_id="repo",
            revision="rev",
            path=path,
            extension=".py",
            language="python",
            size_bytes=len(content.encode("utf-8")),
            line_count=len(content.splitlines()),
            content_hash=f"hash-{path}",
        ),
        raw_content=content,
    )


@pytest.fixture
def files() -> list[RepositoryFile]:
    return [
        make_file("src/billing.py", BILLING_FILE),
        make_file("src/auth.py", AUTH_FILE),
    ]


@pytest.fixture
def issue() -> Issue:
    return Issue(
        id="issue-1",
        repository_id="repo",
        title="apply_discount returns the wrong invoice total",
        body="InvoiceCalculator.apply_discount computes a wrong discount for invoices.",
        labels=["bug"],
        expected_files=["src/billing.py"],
    )


def fake_embed(
    chunks: list[CodeChunk],
    metadata: dict[str, StructuralMetadata],
) -> list[ChunkEmbedding]:
    """Score a chunk on how much 'discount' it talks about, in two dimensions."""
    del metadata
    embeddings = []
    for chunk in chunks:
        discount = float(chunk.content.lower().count("discount"))
        embeddings.append(
            ChunkEmbedding(
                chunk_id=chunk.id,
                embedding_model="fake",
                vector=[discount, 1.0],
            )
        )
    return embeddings


def make_config(**overrides: object) -> ExperimentConfig:
    defaults: dict[str, object] = {
        "name": "two_stage_test",
        "use_bm25": True,
        "use_dense": False,
        "use_ast": True,
        "use_rrf": True,
        "use_reranker": False,
        "use_two_stage": True,
        "doc_use_bm25": True,
        "doc_use_dense": False,
        "doc_top_k": 1,
        "final_top_k": 3,
    }
    defaults.update(overrides)
    return ExperimentConfig(**defaults)  # type: ignore[arg-type]


def test_document_chunk_covers_the_whole_file(files: list[RepositoryFile]) -> None:
    document = chunk_file_as_document(files[0])

    assert document is not None
    assert document.chunk_type == "file"
    assert document.content == BILLING_FILE
    assert (document.start_line, document.end_line) == (1, len(BILLING_FILE.splitlines()))


def test_blank_files_produce_no_documents() -> None:
    assert build_document_chunks([make_file("src/empty.py", "\n  \n")]) == []


def test_stage_one_selects_documents_without_ast_chunking(
    files: list[RepositoryFile],
    issue: Issue,
) -> None:
    config = make_config()
    index = build_document_index(files, config)

    documents = select_documents(issue=issue, index=index, config=config)

    assert [document.path for document in documents] == ["src/billing.py"]
    assert all(document.chunk_id.startswith("chunk_doc_") for document in documents)
    # Stage 1 ranks whole files: one document per file, never an AST chunk.
    assert {chunk.chunk_type for chunk in index.documents} == {"file"}


def test_two_stage_returns_ast_chunks_from_the_selected_document(
    files: list[RepositoryFile],
    issue: Issue,
) -> None:
    config = make_config()
    index = build_document_index(files, config)
    expander = make_document_expander(index, config, chunking=ChunkingConfig())

    result = run_two_stage_retrieval(issue, index, config, expander=expander)
    evidence = result.evidence.evidence_chunks

    assert [document.path for document in result.documents] == ["src/billing.py"]
    assert evidence, "expected chunk-level evidence from the selected document"
    # Stage 3 narrows the document down to specific code regions, all from that file.
    assert {chunk.path for chunk in evidence} == {"src/billing.py"}
    assert evidence[0].symbol_name == "apply_discount"
    file_lines = len(BILLING_FILE.splitlines())
    assert all(chunk.end_line - chunk.start_line < file_lines for chunk in evidence)


def test_stage_two_only_chunks_the_selected_documents(
    files: list[RepositoryFile],
    issue: Issue,
) -> None:
    config = make_config()
    index = build_document_index(files, config)
    expander = make_document_expander(index, config, chunking=ChunkingConfig())

    run_two_stage_retrieval(issue, index, config, expander=expander)

    assert expander.chunked_file_count == 1  # auth.py is never parsed


def test_expander_caches_chunks_and_embeddings_across_issues(
    files: list[RepositoryFile],
    issue: Issue,
) -> None:
    config = make_config(use_dense=True, doc_use_dense=True, doc_use_bm25=False)
    embed_calls: list[int] = []

    def counting_embed(chunks, metadata):  # type: ignore[no-untyped-def]
        embed_calls.append(len(chunks))
        return fake_embed(chunks, metadata)

    index = build_document_index(files, config, embed_chunks_fn=counting_embed)
    expander = make_document_expander(
        index,
        config,
        chunking=ChunkingConfig(),
        embed_chunks_fn=counting_embed,
    )
    query_vector = [1.0, 0.0]  # "discount", nothing else

    first = run_two_stage_retrieval(
        issue, index, config, expander=expander, query_vector=query_vector
    )
    calls_after_first = len(embed_calls)
    second = run_two_stage_retrieval(
        issue, index, config, expander=expander, query_vector=query_vector
    )

    assert [document.path for document in first.documents] == ["src/billing.py"]
    assert first.evidence.evidence_chunks
    assert len(embed_calls) == calls_after_first  # second issue re-uses the cached chunks
    assert [chunk.chunk_id for chunk in second.evidence.evidence_chunks] == [
        chunk.chunk_id for chunk in first.evidence.evidence_chunks
    ]


def test_dense_document_retrieval_requires_a_query_vector(
    files: list[RepositoryFile],
    issue: Issue,
) -> None:
    config = make_config(doc_use_dense=True, doc_use_bm25=False)
    index = build_document_index(files, config, embed_chunks_fn=fake_embed)

    with pytest.raises(ValueError, match="query_vector"):
        select_documents(issue=issue, index=index, config=config)


def test_expander_falls_back_to_window_chunks_for_unparsable_files(issue: Issue) -> None:
    unknown = RepositoryFile(
        metadata=FileMetadata(
            id="repo:rev:notes.txt",
            repository_id="repo",
            revision="rev",
            path="notes.txt",
            extension=".txt",
            language="unknown",
            size_bytes=10,
            line_count=2,
            content_hash="hash-notes",
            is_docs=True,
        ),
        raw_content="discount notes\nsecond line",
    )
    expander = DocumentExpander(
        files_by_id={unknown.metadata.id: unknown},
        chunking=ChunkingConfig(max_chunk_lines=1, overlap_lines=0),
    )

    expanded = expander.expand([unknown.metadata.id], with_embeddings=False)

    assert [chunk.chunk_type for chunk in expanded.chunks] == ["fixed_window", "fixed_window"]


def test_two_stage_config_requires_a_document_retriever() -> None:
    with pytest.raises(ValueError, match="at least one document retriever"):
        make_config(doc_use_bm25=False, doc_use_dense=False, doc_use_ast=False)


def make_chunk(chunk_id: str, file_id: str) -> CodeChunk:
    return CodeChunk(
        id=chunk_id,
        repository_id="repo",
        file_id=file_id,
        path=f"src/{file_id}.py",
        language="python",
        chunk_type="ast",
        start_line=1,
        end_line=5,
        content="pass",
        content_hash=f"hash-{chunk_id}",
    )


def make_document(file_id: str, rank: int) -> DocumentCandidate:
    return DocumentCandidate(
        chunk_id=f"chunk_doc_{file_id}",
        file_id=file_id,
        path=f"src/{file_id}.py",
        language="python",
        rank=rank,
        score=1.0 / rank,
        source="rrf",
    )


def test_document_prior_promotes_chunks_of_the_best_document() -> None:
    """Two chunks the chunk stage scores identically: the better document wins."""
    config = make_config(doc_top_k=2, rrf_k=1, doc_prior_weight=1.0)
    chunks_by_id = {
        "chunk_top": make_chunk("chunk_top", "billing"),
        "chunk_low": make_chunk("chunk_low", "auth"),
    }
    documents = [make_document("auth", rank=1), make_document("billing", rank=2)]
    candidates = [
        RetrievalResult(chunk_id="chunk_top", rank=1, score=0.02, source="rrf", rrf_score=0.02),
        RetrievalResult(chunk_id="chunk_low", rank=2, score=0.02, source="rrf", rrf_score=0.02),
    ]

    rescored = apply_document_prior(candidates, chunks_by_id, documents, config)

    # chunk_low sits in the rank-1 document, so its prior (1/2) beats chunk_top's (1/3).
    assert [result.chunk_id for result in rescored] == ["chunk_low", "chunk_top"]
    assert [result.rank for result in rescored] == [1, 2]
    assert rescored[0].rrf_score == rescored[0].score


def test_document_prior_is_disabled_at_zero_weight() -> None:
    config = make_config(doc_prior_weight=0.0)
    chunks_by_id = {"chunk_a": make_chunk("chunk_a", "billing")}
    candidates = [RetrievalResult(chunk_id="chunk_a", rank=1, score=0.02, source="rrf")]

    assert apply_document_prior(candidates, chunks_by_id, [], config) == candidates
