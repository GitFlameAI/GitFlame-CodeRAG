from pathlib import Path

from gitflame_coderag.ingestion.files import build_file_metadata
from gitflame_coderag.pipelines.two_stage import run_two_stage_retrieval
from gitflame_coderag.retrieval.file_level import build_file_index
from gitflame_coderag.schemas import (
    AIConfig,
    ExperimentConfig,
    Issue,
    RepositoryFile,
    TwoStageConfig,
)


def make_file(path: str, content: str) -> RepositoryFile:
    return RepositoryFile(
        metadata=build_file_metadata(Path(path), content, "repo", "rev", relative_path=path),
        raw_content=content,
    )


CORPUS = [
    make_file(
        "app/auth/tokens.py",
        "def validate_reset_token(token):\n"
        "    if token.is_expired():\n"
        "        raise InvalidTokenError()\n"
        "    return token.user_id\n",
    ),
    make_file(
        "app/billing/invoices.py",
        "def render_invoice(invoice):\n    return invoice.total\n",
    ),
    make_file(
        "app/search/indexer.py",
        "def reindex(documents):\n    return [d.id for d in documents]\n",
    ),
]

ISSUE = Issue(
    id="issue_1",
    repository_id="repo",
    title="validate_reset_token accepts expired tokens",
    body="Password reset accepts an expired token instead of raising InvalidTokenError.",
    expected_files=["app/auth/tokens.py"],
)


def make_config(
    *,
    file_top_n: int,
    max_chunks_per_file: int | None = None,
    min_relevance_score: float | None = None,
    max_context_files: int | None = None,
    max_context_tokens: int | None = None,
) -> TwoStageConfig:
    return TwoStageConfig(
        name="bm25_only",
        file_top_n=file_top_n,
        max_chunks_per_file=max_chunks_per_file,
        min_relevance_score=min_relevance_score,
        max_context_files=max_context_files,
        max_context_tokens=max_context_tokens,
        stage2=ExperimentConfig(
            name="bm25_only",
            use_bm25=True,
            use_dense=False,
            use_ast=False,
            use_rrf=False,
            use_reranker=False,
            final_top_k=5,
        ),
    )


def run(config: TwoStageConfig):
    return run_two_stage_retrieval(
        ISSUE,
        file_index=build_file_index(CORPUS),
        files_by_path={file.metadata.path: file for file in CORPUS},
        ai_config=AIConfig(),
        config=config,
        query_text=f"{ISSUE.title}\n{ISSUE.body}",
    )


def test_two_stage_returns_chunks_of_the_expected_file() -> None:
    result = run(make_config(file_top_n=2))

    paths = {chunk.path for chunk in result.evidence.evidence_chunks}
    assert "app/auth/tokens.py" in paths


def test_stage2_only_ever_sees_the_stage1_candidates() -> None:
    """The point of the split: chunking cost is paid for N files, not the repository."""
    result = run(make_config(file_top_n=1))

    assert result.candidate_paths == ["app/auth/tokens.py"]
    assert {chunk.path for chunk in result.evidence.evidence_chunks} == {"app/auth/tokens.py"}
    assert result.timings["stage1_sec"] >= 0.0


def test_a_query_matching_nothing_yields_no_evidence() -> None:
    result = run_two_stage_retrieval(
        ISSUE,
        file_index=build_file_index(CORPUS),
        files_by_path={file.metadata.path: file for file in CORPUS},
        ai_config=AIConfig(),
        config=make_config(file_top_n=5),
        query_text="zzzz qqqq",
    )

    assert result.evidence.evidence_chunks == []
    assert result.stage1_candidates == []
    assert result.n_candidate_chunks == 0


def test_per_file_cap_limits_one_file_to_its_share_of_the_evidence() -> None:
    capped = run(make_config(file_top_n=3, max_chunks_per_file=1))

    per_file = [chunk.path for chunk in capped.evidence.evidence_chunks]
    assert len(per_file) == len(set(per_file))


def test_two_stage_exposes_context_selection_stats() -> None:
    result = run(make_config(file_top_n=3, max_context_files=1))

    assert result.context_selection.selected_count == len(result.evidence.evidence_chunks)
    assert result.context_selection.selected_file_count == 1


def test_score_gate_can_abstain_instead_of_forcing_top_k() -> None:
    result = run(make_config(file_top_n=3, min_relevance_score=10_000.0))

    assert result.evidence.evidence_chunks == []
    assert result.context_selection.below_score > 0
