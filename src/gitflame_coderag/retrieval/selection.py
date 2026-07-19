"""Deterministic context selection after retrieval ranking.

Retrievers answer "which chunks rank highest?"; this module answers the separate
production question "which of those chunks are allowed into the model context?".
All limits are optional so experiment configurations keep their historical
behaviour unless a context policy is explicitly enabled.
"""

from __future__ import annotations

from dataclasses import dataclass

from gitflame_coderag.chunking.ast_grep import estimate_token_count
from gitflame_coderag.schemas import CodeChunk, RetrievalResult


@dataclass(frozen=True)
class ContextSelectionStats:
    candidate_count: int
    selected_count: int
    selected_file_count: int
    selected_tokens: int
    below_score: int = 0
    file_limit: int = 0
    per_file_limit: int = 0
    token_limit: int = 0
    overlap: int = 0
    missing_chunk: int = 0


@dataclass(frozen=True)
class ContextSelectionResult:
    results: list[RetrievalResult]
    stats: ContextSelectionStats


def select_context_results(
    results: list[RetrievalResult],
    chunks_by_id: dict[str, CodeChunk],
    *,
    max_chunks: int,
    min_relevance_score: float | None = None,
    max_files: int | None = None,
    max_chunks_per_file: int | None = None,
    max_tokens: int | None = None,
    deduplicate_overlaps: bool = False,
    overlap_threshold: float = 0.8,
) -> ContextSelectionResult:
    """Apply hard context budgets without changing retrieval order.

    ``min_relevance_score`` is deliberately score-agnostic: it compares the final
    ``RetrievalResult.score`` emitted by the configured pipeline. Callers must only
    enable it after calibrating that score type; an RRF score is not a probability.

    Token packing is strict. A chunk that would overflow the remaining budget is
    skipped, allowing a smaller lower-ranked chunk to fill the space.
    """
    _validate_limits(
        max_chunks=max_chunks,
        max_files=max_files,
        max_chunks_per_file=max_chunks_per_file,
        max_tokens=max_tokens,
        overlap_threshold=overlap_threshold,
    )

    selected: list[RetrievalResult] = []
    selected_chunks: dict[str, list[CodeChunk]] = {}
    per_file: dict[str, int] = {}
    selected_tokens = 0
    dropped = {
        "below_score": 0,
        "file_limit": 0,
        "per_file_limit": 0,
        "token_limit": 0,
        "overlap": 0,
        "missing_chunk": 0,
    }

    for result in results:
        if min_relevance_score is not None and result.score < min_relevance_score:
            dropped["below_score"] += 1
            continue

        chunk = chunks_by_id.get(result.chunk_id)
        if chunk is None:
            dropped["missing_chunk"] += 1
            continue

        path = chunk.path
        if path not in per_file and max_files is not None and len(per_file) >= max_files:
            dropped["file_limit"] += 1
            continue

        if max_chunks_per_file is not None and per_file.get(path, 0) >= max_chunks_per_file:
            dropped["per_file_limit"] += 1
            continue

        if deduplicate_overlaps and any(
            _line_overlap_ratio(chunk, previous) >= overlap_threshold
            for previous in selected_chunks.get(path, [])
        ):
            dropped["overlap"] += 1
            continue

        chunk_tokens = chunk.token_count or estimate_token_count(chunk.content)
        if max_tokens is not None and selected_tokens + chunk_tokens > max_tokens:
            dropped["token_limit"] += 1
            continue

        per_file[path] = per_file.get(path, 0) + 1
        selected_chunks.setdefault(path, []).append(chunk)
        selected_tokens += chunk_tokens
        selected.append(result.model_copy(update={"rank": len(selected) + 1}))
        if len(selected) >= max_chunks:
            break

    stats = ContextSelectionStats(
        candidate_count=len(results),
        selected_count=len(selected),
        selected_file_count=len(per_file),
        selected_tokens=selected_tokens,
        **dropped,
    )
    return ContextSelectionResult(results=selected, stats=stats)


def _line_overlap_ratio(left: CodeChunk, right: CodeChunk) -> float:
    overlap = max(
        0,
        min(left.end_line, right.end_line) - max(left.start_line, right.start_line) + 1,
    )
    if overlap == 0:
        return 0.0
    left_lines = left.end_line - left.start_line + 1
    right_lines = right.end_line - right.start_line + 1
    return overlap / min(left_lines, right_lines)


def _validate_limits(
    *,
    max_chunks: int,
    max_files: int | None,
    max_chunks_per_file: int | None,
    max_tokens: int | None,
    overlap_threshold: float,
) -> None:
    for name, value in (
        ("max_chunks", max_chunks),
        ("max_files", max_files),
        ("max_chunks_per_file", max_chunks_per_file),
        ("max_tokens", max_tokens),
    ):
        if value is not None and value < 1:
            raise ValueError(f"{name} must be at least 1")
    if not 0.0 < overlap_threshold <= 1.0:
        raise ValueError("overlap_threshold must be in (0, 1]")
