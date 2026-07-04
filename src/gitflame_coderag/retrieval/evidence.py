"""Build final top-k evidence chunks from ranked retrieval results."""

from __future__ import annotations

from gitflame_coderag.schemas import (
    CodeChunk,
    EvidenceBuildResult,
    EvidenceBuildWarning,
    EvidenceChunk,
    EvidenceScores,
    RetrievalResult,
)

SOURCE_SIGNAL_ORDER = ("bm25", "dense", "ast", "rrf", "reranker")


def build_evidence_chunks(
    results: list[RetrievalResult],
    chunks_by_id: dict[str, CodeChunk],
    top_k: int | None = None,
) -> EvidenceBuildResult:
    """Convert ranked retrieval results into final evidence chunks.

    Missing chunks are reported as warnings instead of raising, so long experiment
    runs can continue while still surfacing data consistency problems.
    """
    if top_k is not None and top_k <= 0:
        return EvidenceBuildResult(evidence_chunks=[])

    evidence_chunks: list[EvidenceChunk] = []
    warnings: list[EvidenceBuildWarning] = []

    for result in results:
        chunk = chunks_by_id.get(result.chunk_id)
        if chunk is None:
            warnings.append(
                EvidenceBuildWarning(
                    code="missing_chunk",
                    message="Missing chunk for retrieval result",
                    chunk_id=result.chunk_id,
                )
            )
            continue

        scores = build_evidence_scores(result)
        evidence_chunks.append(
            EvidenceChunk(
                chunk_id=chunk.id,
                repository_id=chunk.repository_id,
                path=chunk.path,
                language=chunk.language,
                node_type=chunk.node_type,
                symbol_name=chunk.symbol_name,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                content=chunk.content,
                scores=scores,
                source_signals=build_source_signals(scores),
            )
        )

        if top_k is not None and len(evidence_chunks) >= top_k:
            break

    return EvidenceBuildResult(evidence_chunks=evidence_chunks, warnings=warnings)


def build_evidence_scores(result: RetrievalResult) -> EvidenceScores:
    """Map retrieval-stage scores onto the final evidence score contract."""
    return EvidenceScores(
        bm25=_score_or_primary(result, "bm25", result.bm25_score),
        dense=_score_or_primary(result, "dense", result.dense_score),
        ast=_score_or_primary(result, "ast", result.ast_score),
        rrf=_score_or_primary(result, "rrf", result.rrf_score),
        reranker=_score_or_primary(result, "reranker", result.reranker_score),
    )


def build_source_signals(
    scores: EvidenceScores,
) -> list[str]:
    """Return retrieval signals that contributed visible scores to the evidence."""
    return [signal for signal in SOURCE_SIGNAL_ORDER if getattr(scores, signal) is not None]


def _score_or_primary(
    result: RetrievalResult,
    source: str,
    score: float | None,
) -> float | None:
    if score is not None:
        return score
    if result.source == source:
        return result.score
    return None
