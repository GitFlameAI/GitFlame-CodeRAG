from gitflame_coderag.retrieval.dense import cosine_similarity
from gitflame_coderag.retrieval.rrf import rrf_fusion
from gitflame_coderag.schemas import RetrievalResult


def test_cosine_similarity() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_rrf_rewards_chunks_returned_by_multiple_rankers() -> None:
    bm25 = [
        RetrievalResult(chunk_id="a", rank=1, score=10.0, source="bm25"),
        RetrievalResult(chunk_id="b", rank=2, score=8.0, source="bm25"),
    ]
    dense = [
        RetrievalResult(chunk_id="b", rank=1, score=0.9, source="dense"),
        RetrievalResult(chunk_id="c", rank=2, score=0.8, source="dense"),
    ]

    fused = rrf_fusion([bm25, dense], top_k=3)

    assert fused[0].chunk_id == "b"
    assert fused[0].source == "rrf"

