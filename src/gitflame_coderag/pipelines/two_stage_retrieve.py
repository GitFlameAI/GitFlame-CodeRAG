"""Two-stage issue retrieval: document selection -> AST split -> chunk retrieval.

Recall is highest when a file is indexed as one whole document, because no
relevant line can fall outside a chunk boundary. Precision, on the other hand,
needs chunks the size of a function. This pipeline gets both:

1. **Stage 1 (documents, no AST-Grep).** Rank whole files with BM25 and dense
   retrieval and keep the top ``doc_top_k`` of them. This stage decides *where*
   the answer lives and is the one that carries recall.
2. **Stage 2 (AST split).** Split only those selected files with AST-Grep, so the
   parsing and embedding cost is paid for a handful of files instead of the repo.
3. **Stage 3 (chunks).** Run the regular BM25/dense/AST + RRF + reranker pipeline
   over the chunks of the selected files to pin down the exact code regions.

Stages 1 and 3 share the issue query vector, so dense retrieval embeds the query
once. Chunking and chunk embeddings are cached per file by :class:`DocumentExpander`,
which keeps the cost of stage 2 near zero when many issues select the same file.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.chunking.document import build_document_chunks
from gitflame_coderag.chunking.pipeline import build_file_chunks
from gitflame_coderag.embeddings import embed_chunks
from gitflame_coderag.pipelines.retrieve_issue import (
    build_issue_keywords,
    build_issue_query,
    collect_enabled_rankings,
    finalize_candidates,
)
from gitflame_coderag.retrieval.ast import ast_candidate_search
from gitflame_coderag.retrieval.bm25 import BM25Index, bm25_search, build_bm25_index
from gitflame_coderag.retrieval.dense import dense_search
from gitflame_coderag.retrieval.evidence import build_evidence_chunks
from gitflame_coderag.retrieval.reranker import CrossEncoderLike
from gitflame_coderag.retrieval.rrf import rrf_fusion
from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ChunkingConfig,
    CodeChunk,
    DocumentCandidate,
    EvidenceBuildResult,
    ExperimentConfig,
    Issue,
    RepositoryFile,
    RetrievalResult,
    StructuralMetadata,
    TwoStageRetrievalResult,
)

EmbedChunksFn = Callable[
    [list[CodeChunk], dict[str, StructuralMetadata]],
    list[ChunkEmbedding],
]


def make_chunk_embedder(config: ExperimentConfig) -> EmbedChunksFn:
    """Bind the configured embedding model into an :data:`EmbedChunksFn`."""

    def embed(
        chunks: list[CodeChunk],
        metadata: dict[str, StructuralMetadata],
    ) -> list[ChunkEmbedding]:
        return embed_chunks(
            chunks,
            metadata,
            model_name=config.embedding_model,
            batch_size=config.embedding_batch_size,
        )

    return embed


@dataclass
class DocumentIndex:
    """Stage-1 index: one whole-file document per repository file.

    Built once per repository revision and reused across issues. The BM25 index is
    built lazily on first use, and ``embeddings`` is empty when dense document
    retrieval is disabled.
    """

    documents: list[CodeChunk]
    metadata: dict[str, StructuralMetadata]
    embeddings: list[ChunkEmbedding]
    files_by_id: dict[str, RepositoryFile]
    _bm25_index: BM25Index | None = field(default=None, init=False, repr=False)

    def bm25_index(self) -> BM25Index:
        if self._bm25_index is None:
            self._bm25_index = build_bm25_index(self.documents, self.metadata)
        return self._bm25_index


@dataclass(frozen=True)
class ExpandedChunks:
    """Chunks of the selected documents, ready for stage-3 retrieval."""

    chunks: list[CodeChunk]
    metadata: dict[str, StructuralMetadata]
    embeddings: list[ChunkEmbedding]


@dataclass
class DocumentExpander:
    """Stage 2: AST-split selected documents, caching the result per file.

    ``embed_chunks_fn`` is only called for files whose chunks are not cached yet,
    and only when the caller asks for embeddings, so a repo's files are chunked and
    embedded at most once no matter how many issues select them.
    """

    files_by_id: dict[str, RepositoryFile]
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    embed_chunks_fn: EmbedChunksFn | None = None
    _chunks_by_file_id: dict[str, list[CodeChunk]] = field(default_factory=dict, init=False)
    _metadata: dict[str, StructuralMetadata] = field(default_factory=dict, init=False)
    _embeddings: dict[str, ChunkEmbedding] = field(default_factory=dict, init=False)

    @property
    def chunked_file_count(self) -> int:
        return len(self._chunks_by_file_id)

    @property
    def cached_chunk_count(self) -> int:
        return sum(len(chunks) for chunks in self._chunks_by_file_id.values())

    def expand(self, file_ids: list[str], *, with_embeddings: bool) -> ExpandedChunks:
        """Return the AST chunks of ``file_ids``, chunking uncached files first."""
        self._chunk_missing_files(file_ids)

        chunks = [
            chunk
            for file_id in file_ids
            for chunk in self._chunks_by_file_id.get(file_id, [])
        ]
        metadata = {chunk.id: self._metadata[chunk.id] for chunk in chunks}

        embeddings: list[ChunkEmbedding] = []
        if with_embeddings and chunks:
            self._embed_missing_chunks(chunks, metadata)
            embeddings = [self._embeddings[chunk.id] for chunk in chunks]

        return ExpandedChunks(chunks=chunks, metadata=metadata, embeddings=embeddings)

    def _chunk_missing_files(self, file_ids: list[str]) -> None:
        for file_id in file_ids:
            if file_id in self._chunks_by_file_id:
                continue
            file = self.files_by_id.get(file_id)
            if file is None:
                self._chunks_by_file_id[file_id] = []
                continue

            chunks = build_file_chunks(file, self.chunking)
            self._chunks_by_file_id[file_id] = chunks
            for chunk in chunks:
                self._metadata[chunk.id] = extract_structural_metadata(chunk)

    def _embed_missing_chunks(
        self,
        chunks: list[CodeChunk],
        metadata: dict[str, StructuralMetadata],
    ) -> None:
        missing = [chunk for chunk in chunks if chunk.id not in self._embeddings]
        if not missing:
            return
        if self.embed_chunks_fn is None:
            raise ValueError("Dense retrieval requires an embed_chunks_fn on the expander")

        for embedding in self.embed_chunks_fn(missing, metadata):
            self._embeddings[embedding.chunk_id] = embedding


def build_document_index(
    files: list[RepositoryFile],
    config: ExperimentConfig,
    *,
    embed_chunks_fn: EmbedChunksFn | None = None,
) -> DocumentIndex:
    """Build the stage-1 whole-file index for one repository revision.

    Document embeddings are computed only when ``config.doc_use_dense`` is set;
    ``embed_chunks_fn`` defaults to the model named by ``config.embedding_model``.
    """
    documents = build_document_chunks(files)
    metadata = {document.id: extract_structural_metadata(document) for document in documents}

    embeddings: list[ChunkEmbedding] = []
    if config.doc_use_dense and documents:
        embed = embed_chunks_fn or make_chunk_embedder(config)
        embeddings = embed(documents, metadata)

    return DocumentIndex(
        documents=documents,
        metadata=metadata,
        embeddings=embeddings,
        files_by_id={file.metadata.id: file for file in files},
    )


def make_document_expander(
    index: DocumentIndex,
    config: ExperimentConfig,
    *,
    chunking: ChunkingConfig | None = None,
    embed_chunks_fn: EmbedChunksFn | None = None,
) -> DocumentExpander:
    """Build the stage-2 expander that AST-splits documents on demand."""
    return DocumentExpander(
        files_by_id=index.files_by_id,
        chunking=chunking or ChunkingConfig(),
        embed_chunks_fn=embed_chunks_fn or make_chunk_embedder(config),
    )


def select_documents(
    *,
    issue: Issue,
    index: DocumentIndex,
    config: ExperimentConfig,
    query_vector: list[float] | None = None,
) -> list[DocumentCandidate]:
    """Stage 1: rank whole files and keep the top ``config.doc_top_k``.

    AST-Grep is deliberately not involved here: the whole file is the retrieval
    unit, which is what makes this stage recall-oriented.
    """
    if not index.documents:
        return []

    rankings: list[list[RetrievalResult]] = []

    if config.doc_use_bm25:
        rankings.append(
            bm25_search(
                build_issue_query(issue),
                index.bm25_index(),
                config.doc_bm25_top_k,
            )
        )

    if config.doc_use_dense:
        if query_vector is None:
            raise ValueError("Dense document retrieval requires a precomputed query_vector")
        if not index.embeddings:
            raise ValueError("Dense document retrieval requires document embeddings")
        rankings.append(dense_search(query_vector, index.embeddings, config.doc_dense_top_k))

    if config.doc_use_ast:
        rankings.append(
            ast_candidate_search(
                build_issue_keywords(issue),
                index.documents,
                index.metadata,
                config.doc_ast_top_k,
            )
        )

    results = combine_document_rankings([r for r in rankings if r], config)
    return build_document_candidates(results, index.documents)


def combine_document_rankings(
    rankings: list[list[RetrievalResult]],
    config: ExperimentConfig,
) -> list[RetrievalResult]:
    """Fuse the stage-1 rankings and truncate them to ``config.doc_top_k``."""
    if not rankings:
        return []
    if config.doc_use_rrf:
        return rrf_fusion(rankings, top_k=config.doc_top_k, rrf_k=config.rrf_k)
    if len(rankings) == 1:
        return rankings[0][: config.doc_top_k]
    raise ValueError("Multiple document rankings require RRF fusion")


def build_document_candidates(
    results: list[RetrievalResult],
    documents: list[CodeChunk],
) -> list[DocumentCandidate]:
    """Attach file identity to the ranked stage-1 results."""
    documents_by_id = {document.id: document for document in documents}
    candidates: list[DocumentCandidate] = []

    for result in results:
        document = documents_by_id.get(result.chunk_id)
        if document is None or result.source == "reranker":
            continue
        candidates.append(
            DocumentCandidate(
                chunk_id=document.id,
                file_id=document.file_id,
                path=document.path,
                language=document.language,
                rank=len(candidates) + 1,
                score=result.score,
                source=result.source,
            )
        )

    return candidates


def apply_document_prior(
    candidates: list[RetrievalResult],
    chunks_by_id: dict[str, CodeChunk],
    documents: list[DocumentCandidate],
    config: ExperimentConfig,
) -> list[RetrievalResult]:
    """Fold the stage-1 document rank back into the fused chunk scores.

    The chunk stage ranks the chunks of every selected document from scratch, so on
    its own it cannot tell a chunk of the best-matching file from a chunk of the
    twentieth one — and a large file contributes hundreds of chunks that can crowd
    the smaller, better file out of the final top-k. The document rank is therefore
    cast as one extra RRF vote per chunk, weighted by ``doc_prior_weight``.
    """
    if config.doc_prior_weight <= 0 or not candidates:
        return candidates

    rank_by_file_id = {document.file_id: document.rank for document in documents}
    unranked = len(documents) + 1

    rescored: list[RetrievalResult] = []
    for candidate in candidates:
        chunk = chunks_by_id.get(candidate.chunk_id)
        document_rank = rank_by_file_id.get(chunk.file_id, unranked) if chunk else unranked
        score = candidate.score + config.doc_prior_weight / (config.rrf_k + document_rank)
        update: dict[str, float] = {"score": score}
        if candidate.rrf_score is not None:
            update["rrf_score"] = score
        rescored.append(candidate.model_copy(update=update))

    ordered = sorted(rescored, key=lambda result: (-result.score, result.chunk_id))
    return [
        result.model_copy(update={"rank": rank})
        for rank, result in enumerate(ordered, start=1)
    ]


def run_two_stage_retrieval(
    issue: Issue,
    index: DocumentIndex,
    config: ExperimentConfig,
    *,
    expander: DocumentExpander,
    query_vector: list[float] | None = None,
    reranker_model: CrossEncoderLike | None = None,
) -> TwoStageRetrievalResult:
    """Select documents, AST-split them, and retrieve the final evidence chunks.

    Dense retrieval expects a precomputed ``query_vector`` (same contract as
    :func:`~gitflame_coderag.pipelines.retrieve_issue.run_retrieval_core`); the same
    vector is used for both the document and the chunk stage.
    """
    documents = select_documents(
        issue=issue,
        index=index,
        config=config,
        query_vector=query_vector,
    )
    if not documents:
        return _empty_result(documents)

    expanded = expander.expand(
        _unique_file_ids(documents),
        with_embeddings=config.use_dense,
    )
    if not expanded.chunks:
        return _empty_result(documents)

    chunks_by_id = {chunk.id: chunk for chunk in expanded.chunks}
    rankings = collect_enabled_rankings(
        issue=issue,
        chunks=expanded.chunks,
        metadata_by_chunk_id=expanded.metadata,
        config=config,
        embeddings=expanded.embeddings,
        query_vector=query_vector,
    )
    results = finalize_candidates(
        issue=issue,
        chunks=expanded.chunks,
        rankings=rankings,
        config=config,
        reranker_model=reranker_model,
        rescore_fused=lambda candidates: apply_document_prior(
            candidates,
            chunks_by_id,
            documents,
            config,
        ),
    )
    evidence = build_evidence_chunks(
        results,
        chunks_by_id,
        top_k=config.final_top_k,
    )

    return TwoStageRetrievalResult(
        documents=documents,
        chunk_count=len(expanded.chunks),
        evidence=evidence,
        results=results,
    )


def _unique_file_ids(documents: list[DocumentCandidate]) -> list[str]:
    return list(dict.fromkeys(document.file_id for document in documents))


def _empty_result(documents: list[DocumentCandidate]) -> TwoStageRetrievalResult:
    return TwoStageRetrievalResult(
        documents=documents,
        chunk_count=0,
        evidence=EvidenceBuildResult(evidence_chunks=[]),
        results=[],
    )
