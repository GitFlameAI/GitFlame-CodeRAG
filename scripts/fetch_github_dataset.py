#!/usr/bin/env python3
"""Collect real GitHub repositories into datasets/original_repositories/.

Two commands:

    discover  search GitHub, keep repositories whose source-file count fits the budget,
              and write a manifest. The file count is read from the Git Trees API, so
              nothing oversized is ever downloaded.

    fetch     download each manifest entry at its pinned commit and write
              <repository_id>/{code/, repo.yml}.

``issues.jsonl`` is authored by hand and is never written or overwritten by this script;
fetch just reports which repositories are still missing one.

Set GITHUB_TOKEN (see .env.example): unauthenticated GitHub allows 60 requests/hour,
which is not enough for discovery.

Examples:

    python scripts/fetch_github_dataset.py discover \\
        --language python --language go --min-stars 200 --max-files 100 --limit 10

    python scripts/fetch_github_dataset.py fetch --manifest configs/github_repos.yml
    python scripts/fetch_github_dataset.py fetch --repo encode/httpx --id repo_020_httpx
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from gitflame_coderag.ingestion.github import (
    DEFAULT_MAX_FILE_BYTES,
    DEFAULT_MAX_FILES,
    DEFAULT_MIN_FILES,
    FileFilters,
    GitHubClient,
    GitHubError,
    RepoCandidate,
    RepoSpec,
    build_manifest,
    discover_repositories,
    dump_yaml,
    existing_repository_ids,
    fetch_repository,
    load_manifest,
    next_dataset_index,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "datasets" / "original_repositories"
DEFAULT_MANIFEST = REPO_ROOT / "configs" / "github_repos.yml"


def load_env_file(path: Path) -> None:
    """Load ``KEY=VALUE`` lines from ``.env`` into the environment.

    Nothing else in the project reads ``.env`` (it exists for docker-compose), but
    GITHUB_TOKEN is expected to live there next to DATABASE_URL. Real environment
    variables win, so ``GITHUB_TOKEN=... python scripts/...`` still overrides the file.
    """
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def build_filters(args: argparse.Namespace) -> FileFilters:
    return FileFilters(
        max_files=args.max_files,
        min_files=args.min_files,
        max_file_bytes=args.max_file_bytes,
        include_tests=not args.no_tests,
    )


def format_duration(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


class Progress:
    """Live progress meter for runs that take minutes (100 repositories do).

    On a terminal it keeps one status line in place and prints results above it. When
    the output is redirected it falls back to a status line every ``LOG_EVERY`` checks,
    so a log file stays readable.

    ``done`` counts *processed* items (a skipped repository still moves the bar), which
    is what keeps the ETA honest.
    """

    LOG_EVERY = 25
    REFRESH_SECONDS = 0.2

    def __init__(self, total: int, noun: str, *, client: GitHubClient | None = None) -> None:
        self.total = max(total, 1)
        self.noun = noun
        self.client = client
        self.done = 0
        self.checked = 0
        self.detail = ""
        self.stream = sys.stderr
        self.started = time.monotonic()
        self.live = self.stream.isatty()
        self._painted = 0
        self._rendered_at = 0.0

    def check(self, count: int = 1) -> None:
        """One more candidate inspected (accepted or rejected)."""
        self.checked += count
        self._refresh(self.checked)

    def advance(self, detail: str = "") -> None:
        """One more item processed."""
        self.done += 1
        self.detail = detail or self.detail
        self._refresh(self.done)

    def log(self, message: str) -> None:
        """Print a permanent line without disturbing the status line."""
        self._erase()
        print(message, flush=True)
        if self.live:
            self.render(force=True)

    def _refresh(self, counter: int) -> None:
        """Repaint the status line -- constantly on a tty, sparsely in a log file."""
        if self.live:
            self.render()
        elif counter % self.LOG_EVERY == 0:
            self.render(force=True)

    def close(self) -> None:
        self._erase()

    def _erase(self) -> None:
        if self.live and self._painted:
            self.stream.write("\r" + " " * self._painted + "\r")
            self.stream.flush()
            self._painted = 0

    def render(self, *, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now - self._rendered_at < self.REFRESH_SECONDS:
            return
        self._rendered_at = now
        line = self._status()
        if not self.live:
            print(line, flush=True)
            return
        self._erase()
        self.stream.write(line)
        self.stream.flush()
        self._painted = len(line)

    def _status(self) -> str:
        elapsed = time.monotonic() - self.started
        parts = [f"[{self.done}/{self.total}] {self.noun}"]
        if self.checked:
            parts.append(f"{self.checked} checked")
        parts.append(format_duration(elapsed))
        if self.done:
            remaining = elapsed / self.done * (self.total - self.done)
            parts.append(f"eta {format_duration(remaining)}")
        if self.detail:
            parts.append(self.detail)
        if self.client and self.client.rate_limit_remaining is not None:
            parts.append(f"api {self.client.rate_limit_remaining} left")
        return "  " + " | ".join(parts)


def command_discover(args: argparse.Namespace) -> int:
    client = GitHubClient()
    if not client.authenticated:
        print("warning: no GITHUB_TOKEN -- search is limited to 10 requests/minute\n")

    progress = Progress(args.limit, "found", client=client)

    def on_candidate(candidate: RepoCandidate) -> None:
        progress.check()
        progress.advance()
        progress.log(_format_candidate(candidate))

    def on_reject(repo: str, reason: str) -> None:
        progress.check()
        if args.verbose:
            progress.log(f"  skip {repo}: {reason}")

    try:
        candidates = discover_repositories(
            client,
            languages=args.language,
            filters=build_filters(args),
            limit=args.limit,
            min_stars=args.min_stars,
            max_stars=args.max_stars,
            max_size_kb=args.max_size_kb,
            license_=args.license,
            pushed_after=args.pushed_after,
            min_open_issues=args.min_open_issues,
            search_limit=args.search_limit,
            existing_ids=existing_repository_ids(args.dest),
            start_index=next_dataset_index(args.dest),
            on_candidate=on_candidate,
            on_reject=on_reject,
        )
    finally:
        progress.close()

    if not candidates:
        print(f"\nchecked {progress.checked} repositories, none matched")
        print("loosen the budget: lower --min-stars, raise --max-files or --max-size-kb")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(dump_yaml(build_manifest(candidates)), encoding="utf-8")
    print(
        f"\n{len(candidates)} repositories out of {progress.checked} checked "
        f"in {format_duration(time.monotonic() - progress.started)} -> {_display(args.out)}"
    )
    print(
        f"review the list, then: python {_display(Path(__file__))} fetch --manifest "
        f"{_display(args.out)}"
    )
    return 0


def command_fetch(args: argparse.Namespace) -> int:
    if args.repo:
        specs = [RepoSpec(repo=args.repo, id=args.id or "", ref=args.ref, subdir=args.subdir)]
        if not specs[0].id:
            print("error: --repo requires --id (the dataset directory name)", file=sys.stderr)
            return 2
    else:
        if not args.manifest.exists():
            print(f"error: manifest not found: {_display(args.manifest)}", file=sys.stderr)
            print("run 'discover' first, or pass --repo/--id for a single repository")
            return 2
        specs = load_manifest(args.manifest)

    client = GitHubClient()
    if not client.authenticated:
        print("warning: no GITHUB_TOKEN -- GitHub allows only 60 requests/hour\n")

    filters = build_filters(args)
    args.dest.mkdir(parents=True, exist_ok=True)

    fetched: list[str] = []
    needs_issues: list[str] = []
    skipped: list[tuple[str, str]] = []
    failed: list[tuple[str, str]] = []
    total_files = 0

    progress = Progress(len(specs), "fetched", client=client)
    try:
        for spec in specs:
            progress.detail = spec.repo  # Shown while the tarball is downloading.
            progress.render(force=True)
            try:
                result = fetch_repository(
                    client,
                    spec,
                    args.dest,
                    filters,
                    issues_source=args.issues_source,
                    force=args.force,
                )
            except GitHubError as error:
                failed.append((spec.repo, str(error)))
                progress.advance(f"{total_files} files")
                progress.log(f"FAIL {spec.repo}: {error}")
                continue

            if result.skipped:
                skipped.append((spec.repo, result.skipped))
                progress.advance(f"{total_files} files")
                progress.log(f"skip {spec.repo}: {result.skipped}")
                continue

            fetched.append(spec.id)
            total_files += len(result.files)
            if not result.has_issues:
                needs_issues.append(spec.id)
            languages = ", ".join(result.languages) or "unknown"
            progress.advance(f"{total_files} files")
            progress.log(
                f"ok   {spec.id:<32} {spec.repo} @ {result.commit[:7]}  "
                f"{len(result.files)} files ({languages})"
            )
    finally:
        progress.close()

    print(
        f"\nfetched {len(fetched)}, skipped {len(skipped)}, failed {len(failed)} "
        f"-- {total_files} files in {format_duration(time.monotonic() - progress.started)} "
        f"-> {_display(args.dest)}"
    )
    if needs_issues:
        print(f"\nstill missing issues.jsonl ({len(needs_issues)}, author them by hand):")
        for repository_id in needs_issues:
            print(f"  {_display(args.dest / repository_id / 'issues.jsonl')}")
    return 1 if failed else 0


def _format_candidate(candidate: RepoCandidate) -> str:
    return (
        f"ok   {candidate.id:<32} {candidate.repo:<40} "
        f"{candidate.source_files:>3} files  {candidate.stars:>6}*  "
        f"{candidate.open_issues:>4} issues  {candidate.license or '-'}"
    )


def _display(path: Path) -> str:
    """Repo-relative path when possible, for copy-pasteable output."""
    try:
        return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def add_filter_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--max-files",
        type=int,
        default=DEFAULT_MAX_FILES,
        help=f"max source files per repository, 0 for no cap (default: {DEFAULT_MAX_FILES})",
    )
    parser.add_argument(
        "--min-files",
        type=int,
        default=DEFAULT_MIN_FILES,
        help=f"reject repositories with fewer source files (default: {DEFAULT_MIN_FILES})",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=DEFAULT_MAX_FILE_BYTES,
        help=f"skip files larger than this (default: {DEFAULT_MAX_FILE_BYTES})",
    )
    parser.add_argument(
        "--no-tests", action="store_true", help="exclude test files from code/"
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help=f"dataset directory (default: {_display(DEFAULT_DEST)})",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser(
        "discover", help="search GitHub and write a manifest of matching repositories"
    )
    discover.add_argument(
        "--language",
        action="append",
        required=True,
        help="GitHub language, repeatable (searched round-robin for a balanced dataset)",
    )
    discover.add_argument(
        "--limit", type=int, default=10, help="repositories to keep (default: 10)"
    )
    discover.add_argument("--min-stars", type=int, default=100, help="default: 100")
    discover.add_argument("--max-stars", type=int, default=None)
    discover.add_argument(
        "--max-size-kb",
        type=int,
        default=5000,
        help="repository size pre-filter in KB (default: 5000)",
    )
    discover.add_argument("--license", default=None, help="SPDX key, e.g. mit, apache-2.0")
    discover.add_argument("--pushed-after", default=None, help="ISO date, e.g. 2024-01-01")
    discover.add_argument(
        "--min-open-issues",
        type=int,
        default=0,
        help="keep repositories with at least this many open issues (default: 0)",
    )
    discover.add_argument(
        "--search-limit",
        type=int,
        default=200,
        help="search hits to inspect per language (default: 200)",
    )
    discover.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"manifest to write (default: {_display(DEFAULT_MANIFEST)})",
    )
    discover.add_argument("--verbose", action="store_true", help="report rejected repositories")
    add_filter_arguments(discover)
    discover.set_defaults(func=command_discover)

    fetch = subparsers.add_parser(
        "fetch", help="download repositories from a manifest into the dataset"
    )
    fetch.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"manifest to read (default: {_display(DEFAULT_MANIFEST)})",
    )
    fetch.add_argument("--repo", default=None, help="fetch a single 'owner/name' instead")
    fetch.add_argument("--id", default=None, help="repository_id for --repo, e.g. repo_020_httpx")
    fetch.add_argument("--ref", default=None, help="branch, tag or sha for --repo")
    fetch.add_argument("--subdir", default=None, help="take only this path prefix for --repo")
    fetch.add_argument(
        "--issues-source",
        default="github",
        help="value of issues.source in repo.yml (default: github)",
    )
    fetch.add_argument(
        "--force", action="store_true", help="re-download repositories that already exist"
    )
    add_filter_arguments(fetch)
    fetch.set_defaults(func=command_fetch)

    return parser


def main(argv: list[str] | None = None) -> int:
    load_env_file(REPO_ROOT / ".env")
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except GitHubError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
