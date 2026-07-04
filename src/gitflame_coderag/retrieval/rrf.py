from collections import defaultdict

from gitflame_coderag.schemas import RetrievalResult

COMPONENT_SCORE_FIELDS = {
    "bm25": "bm25_score",
    "dense": "dense_score",
    "ast": "ast_score",
}


def rrf_fusion(
    rankings: list[list[RetrievalResult]],
    top_k: int,
    rrf_k: int = 60,
) -> list[RetrievalResult]:
    """Fuse pre-ranked BM25, dense, and AST results with RRF."""
    if top_k <= 0:
        return []
    if rrf_k < 0:
        raise ValueError("rrf_k must be non-negative")

    scores: dict[str, float] = defaultdict(float)
    component_scores: dict[str, dict[str, float | None]] = defaultdict(dict)

    for ranking in rankings:
        for rank, result in enumerate(_normalize_ranking(ranking), start=1):
            scores[result.chunk_id] += 1.0 / (rrf_k + rank)
            score_field = COMPONENT_SCORE_FIELDS.get(result.source)
            if score_field is not None:
                component_scores[result.chunk_id][score_field] = _component_score(result)

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]
    return [
        RetrievalResult(
            chunk_id=chunk_id,
            rank=rank,
            score=score,
            source="rrf",
            rrf_score=score,
            **component_scores[chunk_id],
        )
        for rank, (chunk_id, score) in enumerate(ordered, start=1)
    ]


def _component_score(result: RetrievalResult) -> float:
    if result.source == "bm25" and result.bm25_score is not None:
        return result.bm25_score
    if result.source == "dense" and result.dense_score is not None:
        return result.dense_score
    if result.source == "ast" and result.ast_score is not None:
        return result.ast_score
    return result.score


def _normalize_ranking(ranking: list[RetrievalResult]) -> list[RetrievalResult]:
    ordered = sorted(
        ranking,
        key=lambda result: (result.rank, -result.score, result.chunk_id),
    )
    seen_chunk_ids: set[str] = set()
    normalized: list[RetrievalResult] = []

    for result in ordered:
        if result.chunk_id in seen_chunk_ids:
            continue
        seen_chunk_ids.add(result.chunk_id)
        normalized.append(result)

    return normalized
