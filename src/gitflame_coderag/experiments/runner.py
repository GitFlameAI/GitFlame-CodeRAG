"""Experiment suite runner for DB-backed retrieval configurations."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from time import perf_counter
from typing import Literal
from uuid import uuid4

from gitflame_coderag.pipelines.retrieve_issue import run_retrieval_from_db
from gitflame_coderag.retrieval.reranker import CrossEncoderLike
from gitflame_coderag.schemas import (
    EvidenceBuildResult,
    ExperimentConfig,
    ExperimentRun,
    RetrievalResult,
)
from gitflame_coderag.storage.repository import CodeRAGRepository


@dataclass(frozen=True)
class ExperimentIssueResult:
    experiment_run_id: str
    config_name: str
    repository_id: str
    revision: str
    issue_id: str
    retrieval_run_id: str | None
    evidence: EvidenceBuildResult | None
    results: list[RetrievalResult]
    latency_seconds: float
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class ExperimentSuiteResult:
    results: list[ExperimentIssueResult]

    @property
    def n_total(self) -> int:
        return len(self.results)

    @property
    def n_failed(self) -> int:
        return sum(1 for result in self.results if not result.ok)

    @property
    def n_succeeded(self) -> int:
        return sum(1 for result in self.results if result.ok)


def run_experiment_suite(
    repository: CodeRAGRepository,
    configs: list[ExperimentConfig],
    repositories: list[tuple[str, str]],
    *,
    issue_ids_by_repository: dict[str, list[str]] | None = None,
    reranker_model: CrossEncoderLike | None = None,
) -> ExperimentSuiteResult:
    """Run retrieval configs over repository issues and persist runs/results.

    The runner intentionally does not compute metrics. It only executes retrieval,
    records latency, keeps per-issue failures isolated, and lets the metrics layer
    consume the saved retrieval runs/results afterwards.
    """
    suite_results: list[ExperimentIssueResult] = []

    for config in configs:
        for repository_id, revision in repositories:
            experiment_run_id = _make_experiment_run_id(config.name, repository_id)
            issue_ids = _resolve_issue_ids(
                repository,
                repository_id,
                issue_ids_by_repository,
            )
            _save_experiment_status(
                repository,
                experiment_run_id=experiment_run_id,
                config=config,
                repository_id=repository_id,
                revision=revision,
                status="running",
                notes=f"issues={len(issue_ids)}",
            )

            for issue_id in issue_ids:
                suite_results.append(
                    _run_one_issue(
                        repository=repository,
                        config=config,
                        repository_id=repository_id,
                        revision=revision,
                        issue_id=issue_id,
                        experiment_run_id=experiment_run_id,
                        reranker_model=reranker_model,
                    )
                )

            run_results = [r for r in suite_results if r.experiment_run_id == experiment_run_id]
            failed = sum(1 for result in run_results if not result.ok)
            _save_experiment_status(
                repository,
                experiment_run_id=experiment_run_id,
                config=config,
                repository_id=repository_id,
                revision=revision,
                status="completed" if failed < len(issue_ids) else "failed",
                notes=f"issues={len(issue_ids)} failed={failed}",
                completed_at=datetime.now(UTC),
            )

    return ExperimentSuiteResult(results=suite_results)


def _resolve_issue_ids(
    repository: CodeRAGRepository,
    repository_id: str,
    issue_ids_by_repository: dict[str, list[str]] | None,
) -> list[str]:
    if issue_ids_by_repository is not None and repository_id in issue_ids_by_repository:
        return issue_ids_by_repository[repository_id]
    return [issue.id for issue in repository.load_issues_for_repository(repository_id)]


def _run_one_issue(
    *,
    repository: CodeRAGRepository,
    config: ExperimentConfig,
    repository_id: str,
    revision: str,
    issue_id: str,
    experiment_run_id: str,
    reranker_model: CrossEncoderLike | None,
) -> ExperimentIssueResult:
    retrieval_run_id = _make_retrieval_run_id(config.name, repository_id, issue_id)
    started = perf_counter()
    try:
        output = run_retrieval_from_db(
            repository,
            issue_id=issue_id,
            repository_id=repository_id,
            revision=revision,
            config=config,
            reranker_model=reranker_model,
            retrieval_run_id=retrieval_run_id,
            experiment_run_id=experiment_run_id,
        )
        latency = perf_counter() - started
        return ExperimentIssueResult(
            experiment_run_id=experiment_run_id,
            config_name=config.name,
            repository_id=repository_id,
            revision=revision,
            issue_id=issue_id,
            retrieval_run_id=output.retrieval_run_id,
            evidence=output.evidence,
            results=output.results,
            latency_seconds=latency,
        )
    except Exception as error:  # noqa: BLE001 - keep long experiment suites running
        latency = perf_counter() - started
        return ExperimentIssueResult(
            experiment_run_id=experiment_run_id,
            config_name=config.name,
            repository_id=repository_id,
            revision=revision,
            issue_id=issue_id,
            retrieval_run_id=retrieval_run_id,
            evidence=None,
            results=[],
            latency_seconds=latency,
            error=f"{type(error).__name__}: {error}",
        )


def _save_experiment_status(
    repository: CodeRAGRepository,
    *,
    experiment_run_id: str,
    config: ExperimentConfig,
    repository_id: str,
    revision: str,
    status: Literal["running", "completed", "failed"],
    notes: str = "",
    completed_at: datetime | None = None,
) -> None:
    repository.save_experiment_run(
        ExperimentRun(
            id=experiment_run_id,
            name=config.name,
            description="DB-backed retrieval experiment run",
            repository_id=repository_id,
            revision=revision,
            ai_config=config.model_dump(mode="json"),
            embedding_model=config.embedding_model,
            status=status,
            notes=notes,
            completed_at=completed_at,
        )
    )


def _make_experiment_run_id(config_name: str, repository_id: str) -> str:
    return f"experiment_{_slug(config_name)}_{_slug(repository_id)}_{uuid4().hex}"


def _make_retrieval_run_id(config_name: str, repository_id: str, issue_id: str) -> str:
    return f"retrieval_{_slug(config_name)}_{_slug(repository_id)}_{_slug(issue_id)}_{uuid4().hex}"


def _slug(value: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return slug or "run"
