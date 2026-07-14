"""Validation of experiment inputs for the Sprint 2 RAG pipeline.

Owner: Kirill. Before any retrieval experiment runs, every repository bundle must
be well-formed: a parseable ``.yml`` config, readable code files, valid issues and
``expected_files`` that actually exist and survive config filtering, plus a
non-empty ``revision``. These checks reuse the Sprint 1 ingestion functions so the
validator sees exactly what the pipeline will load.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from gitflame_coderag.config.loader import load_ai_config, parse_ai_config
from gitflame_coderag.ingestion import (
    filter_files_by_config,
    load_issues,
    load_repository_files,
)

Severity = Literal["error", "warning"]

MIN_ISSUES_PER_REPO = 3
MAX_ISSUES_PER_REPO = 7


@dataclass
class ValidationProblem:
    repository_id: str
    severity: Severity
    code: str
    message: str


@dataclass
class RepositoryValidation:
    repository_id: str
    revision: str
    n_code_files: int = 0
    n_selected_files: int = 0
    n_issues: int = 0
    n_expected_files: int = 0
    n_expected_missing: int = 0
    n_expected_excluded: int = 0
    problems: list[ValidationProblem] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(p.severity == "error" for p in self.problems)

    @property
    def n_errors(self) -> int:
        return sum(1 for p in self.problems if p.severity == "error")

    @property
    def n_warnings(self) -> int:
        return sum(1 for p in self.problems if p.severity == "warning")


def validate_experiment_inputs(
    repo_dir: Path,
    revision: str = "local",
) -> RepositoryValidation:
    """Validate a single repository bundle for experiment readiness.

    Checks the ``.yml`` config, ``code/`` files, ``issues.jsonl`` and the
    ``expected_files`` of every issue (existence + survival of config filtering),
    and that ``revision`` is provided. Returns a structured report; ``.ok`` is
    ``True`` only when there are no errors.
    """
    repo_dir = Path(repo_dir)
    repository_id = repo_dir.name
    report = RepositoryValidation(repository_id=repository_id, revision=revision)

    def add(severity: Severity, code: str, message: str) -> None:
        report.problems.append(ValidationProblem(repository_id, severity, code, message))

    if not revision:
        add("error", "missing_revision", "revision must be a non-empty string")

    # --- config -----------------------------------------------------------
    config_path = repo_dir / "repo.yml"
    config = None
    if not config_path.exists():
        add("error", "missing_config", "repo.yml not found")
    else:
        try:
            config = parse_ai_config(load_ai_config(config_path))
        except Exception as error:  # noqa: BLE001 - report any parse/validation error
            add("error", "invalid_config", f"repo.yml could not be parsed: {error}")

    # --- code files -------------------------------------------------------
    code_dir = repository_source_root(repo_dir)
    files = []
    selected_paths: set[str] = set()
    all_paths: set[str] = set()
    if not code_dir.is_dir():
        add("error", "missing_code", "code/ or src/ directory not found")
    else:
        files = load_repository_files(code_dir, repository_id, revision)
        report.n_code_files = len(files)
        all_paths = {f.metadata.path for f in files}
        if not files:
            add("error", "empty_code", "code/ contains no readable files")
        if config is not None:
            selected = filter_files_by_config(files, config)
            selected_paths = {f.metadata.path for f in selected}
            report.n_selected_files = len(selected_paths)
            if files and not selected_paths:
                add("error", "config_excludes_all", "analysis config filtered out every file")

    # --- issues -----------------------------------------------------------
    issues_path = repo_dir / "issues.jsonl"
    issues = []
    if not issues_path.exists():
        add("error", "missing_issues", "issues.jsonl not found")
    else:
        try:
            issues = load_issues(issues_path, repository_id)
        except Exception as error:  # noqa: BLE001
            add("error", "invalid_issues", f"issues.jsonl could not be parsed: {error}")
    report.n_issues = len(issues)
    if issues and not (MIN_ISSUES_PER_REPO <= len(issues) <= MAX_ISSUES_PER_REPO):
        add(
            "warning",
            "unexpected_issue_count",
            f"expected {MIN_ISSUES_PER_REPO}-{MAX_ISSUES_PER_REPO} issues, found {len(issues)}",
        )

    seen_ids: set[str] = set()
    for issue in issues:
        if issue.id in seen_ids:
            add("error", "duplicate_issue_id", f"duplicate issue id: {issue.id}")
        seen_ids.add(issue.id)
        if not issue.expected_files:
            add("warning", "no_expected_files", f"{issue.id}: no expected_files listed")
        for expected in issue.expected_files:
            report.n_expected_files += 1
            if all_paths and expected not in all_paths:
                report.n_expected_missing += 1
                add(
                    "error",
                    "expected_file_missing",
                    f"{issue.id}: expected_file not found in code/: {expected}",
                )
            elif selected_paths and expected not in selected_paths and expected in all_paths:
                report.n_expected_excluded += 1
                add(
                    "warning",
                    "expected_file_excluded",
                    f"{issue.id}: expected_file excluded by analysis config: {expected}",
                )

    return report


def validate_dataset(
    dataset_root: Path,
    revision: str = "local",
) -> list[RepositoryValidation]:
    """Validate every repository under ``dataset_root``.

    A repository is any descendant directory that contains a ``repo.yml``.
    """
    dataset_root = Path(dataset_root)
    repos = sorted(p.parent for p in dataset_root.rglob("repo.yml") if p.parent.is_dir())
    return [validate_experiment_inputs(repo, revision) for repo in repos]


def repository_source_root(repo_dir: Path) -> Path:
    """Return the directory whose relative paths match issue.expected_files."""
    code_dir = repo_dir / "code"
    if code_dir.is_dir():
        return code_dir
    return repo_dir
