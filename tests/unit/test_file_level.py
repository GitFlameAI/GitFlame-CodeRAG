from pathlib import Path

from gitflame_coderag.ingestion.files import build_file_metadata
from gitflame_coderag.pipelines.two_stage import cap_chunks_per_file
from gitflame_coderag.retrieval.file_level import (
    build_file_index,
    expand_by_references,
    file_search,
)
from gitflame_coderag.schemas import CodeChunk, RepositoryFile, RetrievalResult


def make_file(path: str, content: str) -> RepositoryFile:
    return RepositoryFile(
        metadata=build_file_metadata(Path(path), content, "repo", "rev", relative_path=path),
        raw_content=content,
    )


def make_chunk(chunk_id: str, path: str, start_line: int = 1) -> CodeChunk:
    return CodeChunk(
        id=chunk_id,
        repository_id="repo",
        file_id=path,
        path=path,
        language="java",
        chunk_type="ast",
        start_line=start_line,
        end_line=start_line + 4,
        content="body",
        content_hash=f"hash-{chunk_id}",
    )


def make_result(chunk_id: str, rank: int) -> RetrievalResult:
    return RetrievalResult(chunk_id=chunk_id, rank=rank, score=1.0 / rank, source="rrf")


CORPUS = [
    make_file(
        "src/main/java/org/es/search/SearchService.java",
        "class SearchService { void executeSearch(SearchRequest request) { validateWindow(); } }",
    ),
    make_file(
        "src/main/java/org/es/bulk/TransportBulkAction.java",
        "class TransportBulkAction { EsThreadPoolExecutor executor; void bulk() { executor.run(); } }",
    ),
    # Named by TransportBulkAction but describing none of the vocabulary an issue would use.
    make_file(
        "src/main/java/org/es/concurrent/EsThreadPoolExecutor.java",
        "class EsThreadPoolExecutor { void run() { queue.poll(); } }",
    ),
    make_file(
        "src/main/java/org/es/index/DocumentParser.java",
        "class DocumentParser { void parse(byte[] source) { mapValue(source); } }",
    ),
]


def test_file_search_ranks_the_file_the_issue_names() -> None:
    index = build_file_index(CORPUS)

    results = file_search("executeSearch fails to validate the search window", index, top_k=3)

    assert results[0].path == "src/main/java/org/es/search/SearchService.java"
    assert results[0].rank == 1
    assert all(result.source == "bm25" for result in results)


def test_file_search_returns_nothing_when_no_query_term_is_indexed() -> None:
    index = build_file_index(CORPUS)

    assert file_search("zzzz qqqq", index, top_k=5) == []
    assert file_search("executeSearch", index, top_k=0) == []


def test_expand_by_references_reaches_a_file_bm25_cannot_see() -> None:
    """The mechanism file is named by the seed, never by the issue."""
    index = build_file_index(CORPUS)
    seeds = file_search("bulk action rejects writes", index, top_k=1)
    assert [seed.path for seed in seeds] == ["src/main/java/org/es/bulk/TransportBulkAction.java"]

    expanded = expand_by_references(seeds, index, limit=5)

    assert "src/main/java/org/es/concurrent/EsThreadPoolExecutor.java" in [
        candidate.path for candidate in expanded
    ]
    # Ranks continue from the seed list, and expansion never re-emits a seed.
    assert expanded[0].rank == len(seeds) + 1
    assert expanded[0].source == "reference"
    assert all(candidate.path != seeds[0].path for candidate in expanded)


def test_expand_by_references_is_disabled_by_a_zero_limit() -> None:
    index = build_file_index(CORPUS)
    seeds = file_search("bulk action", index, top_k=1)

    assert expand_by_references(seeds, index, limit=0) == []


def test_build_file_index_can_skip_the_reference_graph() -> None:
    index = build_file_index(CORPUS, build_reference_graph=False)
    seeds = file_search("bulk action", index, top_k=1)

    assert expand_by_references(seeds, index, limit=5) == []
    assert file_search("executeSearch", index, top_k=1)  # BM25 still works


def test_empty_index_is_searchable() -> None:
    index = build_file_index([])

    assert len(index) == 0
    assert file_search("anything", index, top_k=5) == []


def test_cap_chunks_per_file_frees_slots_for_the_next_file() -> None:
    chunks = [
        make_chunk("a1", "SearchService.java", 1),
        make_chunk("a2", "SearchService.java", 20),
        make_chunk("a3", "SearchService.java", 40),
        make_chunk("b1", "DefaultSearchContext.java", 1),
    ]
    ranked = [make_result("a1", 1), make_result("a2", 2), make_result("a3", 3), make_result("b1", 4)]

    capped = cap_chunks_per_file(ranked, {chunk.id: chunk for chunk in chunks}, cap=2)

    assert [result.chunk_id for result in capped] == ["a1", "a2", "b1"]
    # Ranks are renumbered so downstream top-k cuts stay contiguous.
    assert [result.rank for result in capped] == [1, 2, 3]


def test_cap_chunks_per_file_drops_results_without_a_chunk() -> None:
    chunks = {chunk.id: chunk for chunk in [make_chunk("a1", "SearchService.java")]}

    capped = cap_chunks_per_file([make_result("a1", 1), make_result("ghost", 2)], chunks, cap=5)

    assert [result.chunk_id for result in capped] == ["a1"]
