from gitflame_coderag.retrieval.evidence import (
    build_evidence_chunks,
    build_evidence_scores,
    build_source_signals,
)
from gitflame_coderag.schemas import CodeChunk, EvidenceScores, RetrievalResult


def make_chunk(chunk_id: str, path: str = "src/auth.py") -> CodeChunk:
    return CodeChunk(
        id=chunk_id,
        repository_id="repo_1",
        file_id="file_1",
        path=path,
        language="python",
        chunk_type="ast",
        node_type="function_definition",
        symbol_name="validate_session",
        start_line=10,
        end_line=20,
        content="def validate_session(token):\n    return token is not None",
        content_hash=f"hash_{chunk_id}",
        token_count=8,
    )


def test_build_evidence_chunks_maps_result_scores_and_chunk_fields() -> None:
    chunk = make_chunk("chunk_1")
    result = RetrievalResult(
        chunk_id="chunk_1",
        rank=1,
        score=0.91,
        source="reranker",
        bm25_score=12.0,
        dense_score=0.82,
        ast_score=3.0,
        rrf_score=0.048,
        reranker_score=0.91,
    )

    output = build_evidence_chunks([result], {"chunk_1": chunk}, top_k=1)

    assert output.warnings == []
    assert len(output.evidence_chunks) == 1

    evidence = output.evidence_chunks[0]
    assert evidence.chunk_id == "chunk_1"
    assert evidence.repository_id == "repo_1"
    assert evidence.path == "src/auth.py"
    assert evidence.node_type == "function_definition"
    assert evidence.symbol_name == "validate_session"
    assert evidence.start_line == 10
    assert evidence.end_line == 20
    assert evidence.content == chunk.content
    assert evidence.scores.bm25 == 12.0
    assert evidence.scores.dense == 0.82
    assert evidence.scores.ast == 3.0
    assert evidence.scores.rrf == 0.048
    assert evidence.scores.reranker == 0.91
    assert evidence.source_signals == ["bm25", "dense", "ast", "rrf", "reranker"]


def test_build_evidence_chunks_reports_missing_chunks_and_continues() -> None:
    chunk_1 = make_chunk("chunk_1")
    chunk_2 = make_chunk("chunk_2", path="src/cache.py")
    results = [
        RetrievalResult(chunk_id="chunk_1", rank=1, score=0.9, source="rrf"),
        RetrievalResult(chunk_id="missing", rank=2, score=0.8, source="rrf"),
        RetrievalResult(chunk_id="chunk_2", rank=3, score=0.7, source="rrf"),
    ]

    output = build_evidence_chunks(
        results,
        {"chunk_1": chunk_1, "chunk_2": chunk_2},
        top_k=2,
    )

    assert [chunk.chunk_id for chunk in output.evidence_chunks] == ["chunk_1", "chunk_2"]
    assert len(output.warnings) == 1
    assert output.warnings[0].code == "missing_chunk"
    assert output.warnings[0].chunk_id == "missing"


def test_build_evidence_scores_uses_primary_score_when_component_score_is_missing() -> None:
    result = RetrievalResult(chunk_id="chunk_1", rank=1, score=0.5, source="dense")

    scores = build_evidence_scores(result)

    assert scores == EvidenceScores(dense=0.5)
    assert build_source_signals(scores) == ["dense"]


def test_build_evidence_chunks_returns_empty_for_non_positive_top_k() -> None:
    chunk = make_chunk("chunk_1")
    result = RetrievalResult(chunk_id="chunk_1", rank=1, score=0.9, source="rrf")

    output = build_evidence_chunks([result], {"chunk_1": chunk}, top_k=0)

    assert output.evidence_chunks == []
    assert output.warnings == []
