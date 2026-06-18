from collections import defaultdict

from gitflame_coderag.schemas import RetrievalResult


def rrf_fusion(
    rankings: list[list[RetrievalResult]],
    top_k: int,
    rrf_k: int = 60,
) -> list[RetrievalResult]:
    scores: dict[str, float] = defaultdict(float)
    component_scores: dict[str, dict[str, float | None]] = defaultdict(dict)

    for ranking in rankings:
        for rank, result in enumerate(ranking, start=1):
            scores[result.chunk_id] += 1.0 / (rrf_k + rank)
            component_scores[result.chunk_id][f"{result.source}_score"] = result.score

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

