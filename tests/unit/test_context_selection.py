import pytest

from gitflame_coderag.retrieval.selection import select_context_results
from gitflame_coderag.schemas import CodeChunk, RetrievalResult


def make_chunk(
    chunk_id: str,
    path: str,
    start_line: int,
    end_line: int,
    *,
    token_count: int = 10,
) -> CodeChunk:
    return CodeChunk(
        id=chunk_id,
        repository_id="repo",
        file_id=f"file_{path}",
        path=path,
        language="python",
        chunk_type="ast",
        start_line=start_line,
        end_line=end_line,
        content=f"# {chunk_id}\n" * token_count,
        content_hash=f"hash_{chunk_id}",
        token_count=token_count,
    )


def make_result(chunk_id: str, rank: int, score: float) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        rank=rank,
        score=score,
        source="rrf",
        rrf_score=score,
    )


def test_selection_applies_score_gate_and_chunk_limit() -> None:
    chunks = {
        f"c{index}": make_chunk(f"c{index}", f"src/f{index}.py", 1, 5)
        for index in range(1, 5)
    }
    results = [
        make_result("c1", 1, 0.9),
        make_result("c2", 2, 0.7),
        make_result("c3", 3, 0.49),
        make_result("c4", 4, 0.4),
    ]

    selection = select_context_results(
        results,
        chunks,
        max_chunks=2,
        min_relevance_score=0.5,
    )

    assert [result.chunk_id for result in selection.results] == ["c1", "c2"]
    assert [result.rank for result in selection.results] == [1, 2]
    assert selection.stats.selected_count == 2


def test_selection_caps_distinct_files_and_refills_from_existing_file() -> None:
    chunks = {
        "c1": make_chunk("c1", "src/auth.py", 1, 5),
        "c2": make_chunk("c2", "src/cache.py", 1, 5),
        "c3": make_chunk("c3", "src/auth.py", 20, 25),
    }
    results = [
        make_result("c1", 1, 0.9),
        make_result("c2", 2, 0.8),
        make_result("c3", 3, 0.7),
    ]

    selection = select_context_results(results, chunks, max_chunks=3, max_files=1)

    assert [result.chunk_id for result in selection.results] == ["c1", "c3"]
    assert selection.stats.selected_file_count == 1
    assert selection.stats.file_limit == 1


def test_selection_enforces_token_budget_and_overlap_deduplication() -> None:
    chunks = {
        "c1": make_chunk("c1", "src/auth.py", 1, 10, token_count=8),
        "c2": make_chunk("c2", "src/auth.py", 2, 9, token_count=5),
        "c3": make_chunk("c3", "src/cache.py", 1, 5, token_count=4),
        "c4": make_chunk("c4", "src/db.py", 1, 5, token_count=5),
    }
    results = [
        make_result("c1", 1, 0.9),
        make_result("c2", 2, 0.8),
        make_result("c3", 3, 0.7),
        make_result("c4", 4, 0.6),
    ]

    selection = select_context_results(
        results,
        chunks,
        max_chunks=4,
        max_tokens=12,
        deduplicate_overlaps=True,
        overlap_threshold=0.8,
    )

    assert [result.chunk_id for result in selection.results] == ["c1", "c3"]
    assert selection.stats.selected_tokens == 12
    assert selection.stats.overlap == 1
    assert selection.stats.token_limit == 1


def test_selection_reports_missing_chunks_and_validates_limits() -> None:
    missing = make_result("missing", 1, 0.9)

    selection = select_context_results([missing], {}, max_chunks=1)

    assert selection.results == []
    assert selection.stats.missing_chunk == 1
    with pytest.raises(ValueError, match="max_chunks"):
        select_context_results([], {}, max_chunks=0)
