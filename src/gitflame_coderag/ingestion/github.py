"""Collecting real GitHub repositories into the evaluation dataset.

Owner: Kirill (ingestion). Two stages, both driven by ``scripts/fetch_github_dataset.py``:

``discover``
    Search GitHub for candidate repositories and keep only the ones whose *source*
    file count fits the dataset budget. The count comes from the Git Trees API (one
    request per candidate, whole tree in a single response), so oversized repositories
    are rejected before anything is downloaded. Emits a manifest.

``fetch``
    Download the pinned commit as a tarball and write
    ``datasets/original_repositories/<repository_id>/{code/, repo.yml}``.

``issues.jsonl`` is authored by hand and is never written, moved or overwritten here.

File selection reuses ``ingestion.files``: the same extension table that drives
``detect_language`` and the same glob semantics as ``filter_files_by_config``, so the
``analysis.include`` / ``analysis.exclude`` patterns written into ``repo.yml`` select
exactly the files this module copied into ``code/``.
"""

from __future__ import annotations

import io
import json
import os
import re
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from itertools import zip_longest
from pathlib import Path, PurePosixPath
from shutil import rmtree
from typing import Any

import yaml

from gitflame_coderag.ingestion.files import (
    LANGUAGES_BY_EXTENSION,
    _matches,
    detect_language,
    is_test_path,
)

GITHUB_API_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
USER_AGENT = "gitflame-coderag-dataset"

DEFAULT_MAX_FILES = 100
DEFAULT_MIN_FILES = 3
DEFAULT_MAX_FILE_BYTES = 200_000
SEARCH_PAGE_SIZE = 100
SEARCH_RESULT_LIMIT = 1000  # Hard cap of the GitHub search API.

SOURCE_EXTENSIONS = frozenset(LANGUAGES_BY_EXTENSION)

# Vendored, generated and build-output paths. Written verbatim into
# ``analysis.exclude`` in repo.yml, so they must use the glob semantics of
# ``ingestion.files._matches`` (``**/`` matches at any depth).
DEFAULT_EXCLUDE: tuple[str, ...] = (
    "**/.*/**",  # Hidden dirs: .github, .devcontainer, .circleci -- tooling, not the code.
    "**/node_modules/**",
    "**/vendor/**",
    "**/third_party/**",
    "**/dist/**",
    "**/build/**",
    "**/target/**",
    "**/.git/**",
    "**/__pycache__/**",
    "**/site-packages/**",
    "**/.venv/**",
    "*.min.js",
    "*.min.css",
    "*.lock",
    "*_pb2.py",
    "*_pb2_grpc.py",
    "*.pb.go",
)


class GitHubError(RuntimeError):
    """A GitHub request failed and is not worth retrying."""


class GitHubRateLimitError(GitHubError):
    """The rate limit is exhausted and the reset is further away than ``max_wait``."""


@dataclass(frozen=True)
class RepoSpec:
    """One manifest entry: which repository to fetch and how to trim it."""

    repo: str  # "owner/name"
    id: str  # repository_id, also the dataset directory name
    ref: str | None = None  # Branch, tag or commit sha; default branch when None.
    subdir: str | None = None  # Take only this path prefix, re-rooted in code/.


@dataclass(frozen=True)
class TreeEntry:
    """One blob in a repository tree."""

    path: str
    size: int


@dataclass(frozen=True)
class FileFilters:
    """Which files of a repository end up in ``code/``."""

    max_files: int = DEFAULT_MAX_FILES  # 0 disables the cap.
    min_files: int = DEFAULT_MIN_FILES
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    extensions: frozenset[str] = SOURCE_EXTENSIONS
    exclude: tuple[str, ...] = DEFAULT_EXCLUDE
    include_tests: bool = True


@dataclass(frozen=True)
class RepoCandidate:
    """A searched repository that fits the dataset budget."""

    repo: str
    id: str
    ref: str  # Pinned commit sha.
    default_branch: str
    stars: int
    open_issues: int
    license: str | None
    size_kb: int
    source_files: int
    languages: tuple[str, ...]

    def to_spec(self) -> RepoSpec:
        return RepoSpec(repo=self.repo, id=self.id, ref=self.ref)


@dataclass
class FetchResult:
    """Outcome of fetching one repository."""

    spec: RepoSpec
    commit: str = ""
    path: Path | None = None
    files: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    skipped: str | None = None  # Reason, when the repository was not written.
    has_issues: bool = False  # Whether issues.jsonl already exists (authored by hand).


# --------------------------------------------------------------------------- #
# HTTP client
# --------------------------------------------------------------------------- #
class GitHubClient:
    """Minimal GitHub REST client: JSON reads, tarball downloads, retries.

    Authenticates with ``token`` or ``$GITHUB_TOKEN``. Unauthenticated requests are
    limited to 60/hour (and 10/minute for search), which is not enough for discovery,
    so a token is strongly recommended.

    Rate-limit responses are waited out (up to ``max_wait`` seconds) and retried;
    5xx and transient network errors are retried with exponential backoff.
    """

    def __init__(
        self,
        token: str | None = None,
        *,
        api_url: str = GITHUB_API_URL,
        timeout: float = 30.0,
        max_retries: int = 4,
        max_wait: float = 300.0,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN") or None
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_wait = max_wait
        self._sleep = sleep
        # Budget left in the current rate-limit window, as last reported by GitHub.
        # None until the first response. Progress reporting reads these.
        self.rate_limit_remaining: int | None = None
        self.rate_limit_reset: float | None = None
        self.requests_made = 0

    @property
    def authenticated(self) -> bool:
        return self.token is not None

    def _track_rate_limit(self, headers: Any) -> None:
        remaining = headers.get("x-ratelimit-remaining")
        reset = headers.get("x-ratelimit-reset")
        if remaining is not None:
            self.rate_limit_remaining = int(remaining)
        if reset is not None:
            self.rate_limit_reset = float(reset)

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """GET a JSON resource. ``path`` is API-relative (``/repos/owner/name``)."""
        url = self._url(path, params)
        payload, _ = self._request(url, accept="application/vnd.github+json")
        return json.loads(payload.decode("utf-8"))

    def get_bytes(self, path: str, params: dict[str, Any] | None = None) -> bytes:
        """GET a binary resource (tarball). Redirects to codeload are followed."""
        url = self._url(path, params)
        payload, _ = self._request(url, accept="application/vnd.github+json")
        return payload

    def _url(self, path: str, params: dict[str, Any] | None = None) -> str:
        url = path if path.startswith("http") else f"{self.api_url}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        return url

    def _headers(self, accept: str) -> dict[str, str]:
        headers = {
            "Accept": accept,
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": API_VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, url: str, *, accept: str) -> tuple[bytes, dict[str, str]]:
        request = urllib.request.Request(url, headers=self._headers(accept))
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                self.requests_made += 1
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    self._track_rate_limit(response.headers)
                    return response.read(), dict(response.headers)
            except urllib.error.HTTPError as error:
                last_error = error
                self._track_rate_limit(error.headers)
                delay = self._retry_delay(error, attempt)
                if delay is None:
                    raise GitHubError(f"GET {url} -> {error.code} {error.reason}") from error
                self._sleep(delay)
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                last_error = error
                if attempt >= self.max_retries:
                    break
                self._sleep(2.0**attempt)
        raise GitHubError(f"GET {url} failed after {self.max_retries + 1} attempts: {last_error}")

    def _retry_delay(self, error: urllib.error.HTTPError, attempt: int) -> float | None:
        """Seconds to wait before retrying, or None when the error is terminal."""
        if attempt >= self.max_retries:
            return None

        if error.code in (403, 429):
            retry_after = error.headers.get("retry-after")
            if retry_after:
                return min(float(retry_after), self.max_wait)
            # Primary rate limit: remaining==0 and a reset timestamp to wait for.
            if error.headers.get("x-ratelimit-remaining") == "0":
                reset = float(error.headers.get("x-ratelimit-reset", 0))
                wait = max(reset - time.time(), 0.0) + 1.0
                if wait > self.max_wait:
                    hint = "" if self.token else " (set GITHUB_TOKEN to raise the limit)"
                    raise GitHubRateLimitError(
                        f"rate limit exhausted, resets in {wait:.0f}s{hint}"
                    ) from error
                return wait
            return None  # Genuine 403: private repo, bad token, blocked resource.

        if error.code >= 500:
            return 2.0**attempt
        return None


# --------------------------------------------------------------------------- #
# Repository metadata
# --------------------------------------------------------------------------- #
def get_repository(client: GitHubClient, repo: str) -> dict[str, Any]:
    """Fetch repository metadata for ``owner/name``."""
    return client.get_json(f"/repos/{repo}")


def resolve_commit(client: GitHubClient, repo: str, ref: str | None = None) -> str:
    """Resolve a branch, tag or short sha to a full commit sha.

    ``None`` resolves the repository's default branch. The result is what gets pinned
    as ``repository.revision`` in ``repo.yml``, so a re-fetch reproduces the same code.
    """
    target = ref or get_repository(client, repo)["default_branch"]
    payload = client.get_json(f"/repos/{repo}/commits/{urllib.parse.quote(target)}")
    return str(payload["sha"])


def list_tree(client: GitHubClient, repo: str, commit: str) -> list[TreeEntry]:
    """List every blob of a commit in one request (recursive Git Trees API)."""
    payload = client.get_json(f"/repos/{repo}/git/trees/{commit}", {"recursive": "1"})
    if payload.get("truncated"):
        raise GitHubError(
            f"{repo}: tree response truncated (repository too large for the dataset)"
        )
    return [
        TreeEntry(path=item["path"], size=int(item.get("size", 0)))
        for item in payload.get("tree", ())
        if item.get("type") == "blob"
    ]


def download_tarball(client: GitHubClient, repo: str, commit: str) -> bytes:
    """Download a commit as a gzipped tarball (no git, no history)."""
    return client.get_bytes(f"/repos/{repo}/tarball/{commit}")


# --------------------------------------------------------------------------- #
# File selection
# --------------------------------------------------------------------------- #
def select_files(
    entries: Iterable[TreeEntry],
    filters: FileFilters,
    *,
    subdir: str | None = None,
) -> list[TreeEntry]:
    """Keep the source files of a tree that belong in the dataset.

    Applies, in order: the ``subdir`` prefix, the source-extension whitelist, the
    exclude globs, the per-file size cap and (optionally) test exclusion. Returns
    every match — the ``max_files`` budget is enforced by the caller, which needs the
    real count to report why a repository was rejected.
    """
    prefix = _normalize_subdir(subdir)
    selected: list[TreeEntry] = []
    for entry in entries:
        path = entry.path
        if prefix and not path.startswith(f"{prefix}/"):
            continue
        if PurePosixPath(path).suffix.lower() not in filters.extensions:
            continue
        if any(_matches(path, pattern) for pattern in filters.exclude):
            continue
        if filters.max_file_bytes and entry.size > filters.max_file_bytes:
            continue
        if not filters.include_tests and is_test_path(path):
            continue
        selected.append(entry)
    # Shallow files first: a truncated selection stays close to the repository root.
    return sorted(selected, key=lambda item: (item.path.count("/"), item.path))


def _normalize_subdir(subdir: str | None) -> str:
    return (subdir or "").strip("/")


def _relocate(path: str, subdir: str | None) -> str:
    """Re-root a repository path under ``subdir`` (``pkg/a.py`` -> ``a.py``)."""
    prefix = _normalize_subdir(subdir)
    if prefix and path.startswith(f"{prefix}/"):
        return path[len(prefix) + 1 :]
    return path


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #
def extract_files(
    archive: bytes,
    paths: Iterable[str],
    dest: Path,
    *,
    subdir: str | None = None,
) -> list[str]:
    """Extract the selected repository paths from a tarball into ``dest``.

    Members are matched against ``paths`` (repository-relative, as returned by the
    trees API) after stripping the ``owner-name-sha/`` root that GitHub adds. Content
    is written byte-for-byte — never normalized — but files that do not decode as
    UTF-8 are skipped, since chunking and retrieval only handle text.
    """
    wanted = set(paths)
    dest = Path(dest)
    root = dest.resolve()
    written: list[str] = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            repo_path = _strip_archive_root(member.name)
            if repo_path is None or repo_path not in wanted:
                continue
            relative = _relocate(repo_path, subdir)
            target = (dest / relative).resolve()
            if not target.is_relative_to(root):
                continue  # Crafted member name escaping the destination.
            handle = tar.extractfile(member)
            if handle is None:
                continue
            payload = handle.read()
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError:
                continue  # Binary content behind a source extension.
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            written.append(relative)
    return sorted(written)


def _strip_archive_root(name: str) -> str | None:
    """Drop the ``owner-name-sha/`` prefix GitHub puts on every tarball member."""
    _, separator, remainder = name.replace("\\", "/").partition("/")
    if not separator or not remainder:
        return None
    return remainder


# --------------------------------------------------------------------------- #
# repo.yml
# --------------------------------------------------------------------------- #
def language_priority(paths: Iterable[str]) -> list[str]:
    """Languages of the selected files, most frequent first."""
    counts: dict[str, int] = {}
    for path in paths:
        language = detect_language(Path(path), "")
        if language != "unknown":
            counts[language] = counts.get(language, 0) + 1
    return [language for language, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def include_patterns(paths: Iterable[str]) -> list[str]:
    """Derive ``analysis.include`` from the layout of the selected files."""
    patterns: set[str] = set()
    for path in paths:
        head, separator, _ = path.partition("/")
        if separator:
            patterns.add(f"{head}/**")
        else:
            patterns.add(f"*{PurePosixPath(path).suffix.lower()}")
    return sorted(patterns) or ["**/*"]


def build_repo_config(
    metadata: dict[str, Any],
    commit: str,
    paths: list[str],
    *,
    issues_source: str = "github",
    subdir: str | None = None,
) -> dict[str, Any]:
    """Build the ``repo.yml`` mapping for a fetched repository.

    Follows the template in ``context.md``. The ``repository`` section records the
    provenance (url, pinned commit, license, subdir) — ``parse_ai_config`` ignores it,
    but it is what makes a fetched repository reproducible.
    """
    license_info = metadata.get("license") or {}
    repository: dict[str, Any] = {
        "name": metadata.get("name", ""),
        "full_name": metadata.get("full_name", ""),
        "url": metadata.get("html_url", ""),
        "default_branch": metadata.get("default_branch", "main"),
        "revision": commit,
        "license": license_info.get("spdx_id"),
        "stars": metadata.get("stargazers_count", 0),
        "language_priority": language_priority(paths),
    }
    if _normalize_subdir(subdir):
        repository["subdir"] = _normalize_subdir(subdir)

    return {
        "version": 1,
        "repository": repository,
        "analysis": {
            "enabled": True,
            "include": include_patterns(paths),
            "exclude": list(DEFAULT_EXCLUDE),
        },
        "issues": {
            "source": issues_source,
            "format": "github_issue",
            "fields": ["title", "body", "labels", "expected_files"],
        },
        "chunking": {
            "strategy": "ast_aware",
            "fallback_strategy": "fixed_window",
            "max_chunk_lines": 80,
            "overlap_lines": 10,
            "include_metadata": True,
        },
        "ast_grep": {
            "enabled": True,
            "extract_symbols": True,
            "extract_imports": True,
            "extract_handlers": True,
            "extract_tests": True,
        },
        "retrieval": {
            "top_k": 10,
            "use_bm25": True,
            "use_dense": True,
            "use_ast_candidates": True,
            "fusion_method": "rrf",
        },
        "embeddings": {
            "model": "server_controlled",
            "normalize_vectors": True,
            "batch_size": 32,
        },
        "storage": {
            "store_chunks": True,
            "store_embeddings": True,
            "store_retrieval_runs": True,
        },
        "evaluation": {
            "metrics": ["precision_at_k", "recall_at_k", "mrr", "ndcg_at_k"],
        },
    }


def dump_yaml(payload: dict[str, Any]) -> str:
    """Serialize a mapping preserving key order (repo.yml, manifests)."""
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=100)


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #
def fetch_repository(
    client: GitHubClient,
    spec: RepoSpec,
    dest_root: Path,
    filters: FileFilters | None = None,
    *,
    issues_source: str = "github",
    force: bool = False,
) -> FetchResult:
    """Fetch one repository into ``dest_root/<spec.id>/{code/, repo.yml}``.

    Skips (rather than fails) a repository that already exists, has no source files, or
    busts the ``max_files`` budget. ``issues.jsonl`` is never touched: an existing one
    survives a ``--force`` re-fetch, and a missing one is reported via
    ``FetchResult.has_issues`` so the caller can remind the user to author it.
    """
    filters = filters or FileFilters()
    repo_dir = Path(dest_root) / spec.id
    code_dir = repo_dir / "code"
    result = FetchResult(spec=spec, path=repo_dir, has_issues=(repo_dir / "issues.jsonl").exists())

    if code_dir.exists() and not force:
        result.skipped = "already fetched (use --force to refresh)"
        return result

    metadata = get_repository(client, spec.repo)
    commit = resolve_commit(client, spec.repo, spec.ref or metadata["default_branch"])
    result.commit = commit

    selected = select_files(list_tree(client, spec.repo, commit), filters, subdir=spec.subdir)
    if len(selected) < filters.min_files:
        result.skipped = f"only {len(selected)} source files (min {filters.min_files})"
        return result
    if filters.max_files and len(selected) > filters.max_files:
        result.skipped = f"{len(selected)} source files exceed the max of {filters.max_files}"
        return result

    archive = download_tarball(client, spec.repo, commit)
    if code_dir.exists():
        rmtree(code_dir)  # Refresh: drop files that vanished upstream. issues.jsonl survives.
    code_dir.mkdir(parents=True, exist_ok=True)

    written = extract_files(
        archive, [entry.path for entry in selected], code_dir, subdir=spec.subdir
    )
    if not written:
        result.skipped = "no extractable text files"
        return result

    config = build_repo_config(
        metadata, commit, written, issues_source=issues_source, subdir=spec.subdir
    )
    (repo_dir / "repo.yml").write_text(dump_yaml(config), encoding="utf-8")

    result.files = written
    result.languages = config["repository"]["language_priority"]
    return result


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #
def search_repositories(
    client: GitHubClient,
    *,
    language: str,
    min_stars: int = 100,
    max_stars: int | None = None,
    max_size_kb: int | None = 5000,
    license_: str | None = None,
    pushed_after: str | None = None,
    limit: int = SEARCH_RESULT_LIMIT,
) -> Iterator[dict[str, Any]]:
    """Yield search hits for one language, most-starred first.

    Note the search API caps any query at 1000 results; ``size`` is the repository size
    in KB (a cheap pre-filter — the real file-count check happens in
    :func:`discover_repositories`). Forks are excluded by GitHub unless asked for.
    """
    stars = f"{min_stars}..{max_stars}" if max_stars else f">={min_stars}"
    qualifiers = [f"language:{language}", f"stars:{stars}", "is:public", "archived:false"]
    if max_size_kb:
        qualifiers.append(f"size:<={max_size_kb}")
    if license_:
        qualifiers.append(f"license:{license_}")
    if pushed_after:
        qualifiers.append(f"pushed:>={pushed_after}")
    query = " ".join(qualifiers)

    yielded = 0
    limit = min(limit, SEARCH_RESULT_LIMIT)
    for page in range(1, SEARCH_RESULT_LIMIT // SEARCH_PAGE_SIZE + 1):
        payload = client.get_json(
            "/search/repositories",
            {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": SEARCH_PAGE_SIZE,
                "page": page,
            },
        )
        items = payload.get("items", [])
        for item in items:
            if yielded >= limit:
                return
            yield item
            yielded += 1
        if len(items) < SEARCH_PAGE_SIZE:
            return


def discover_repositories(
    client: GitHubClient,
    *,
    languages: list[str],
    filters: FileFilters | None = None,
    limit: int = 10,
    min_stars: int = 100,
    max_stars: int | None = None,
    max_size_kb: int | None = 5000,
    license_: str | None = None,
    pushed_after: str | None = None,
    min_open_issues: int = 0,
    search_limit: int = 200,
    existing_ids: Iterable[str] = (),
    start_index: int = 1,
    on_candidate: Callable[[RepoCandidate], None] | None = None,
    on_reject: Callable[[str, str], None] | None = None,
) -> list[RepoCandidate]:
    """Search GitHub and keep repositories that fit the dataset budget.

    Search qualifiers (language, stars, size, license) narrow the field cheaply; each
    surviving candidate then costs one Git Trees request, which gives the *real* source
    file count — the ``max_files`` budget is applied to that, not to the repository's
    total file count or its size in KB.

    Languages are consumed round-robin so the result stays language-balanced. Failures
    on a single candidate (moved repo, empty tree, truncated tree) are reported through
    ``on_reject`` and never abort the sweep.
    """
    filters = filters or FileFilters()
    searches = [
        search_repositories(
            client,
            language=language,
            min_stars=min_stars,
            max_stars=max_stars,
            max_size_kb=max_size_kb,
            license_=license_,
            pushed_after=pushed_after,
            limit=search_limit,
        )
        for language in languages
    ]

    taken: set[str] = set(existing_ids)
    candidates: list[RepoCandidate] = []
    index = start_index
    for hits in zip_longest(*searches):
        for hit in hits:
            if hit is None:
                continue
            if len(candidates) >= limit:
                return candidates
            repo = hit["full_name"]
            reject = _reject_reason(hit, min_open_issues)
            if reject:
                if on_reject:
                    on_reject(repo, reject)
                continue
            try:
                commit = resolve_commit(client, repo, hit["default_branch"])
                selected = select_files(list_tree(client, repo, commit), filters)
            except GitHubRateLimitError:
                raise
            except GitHubError as error:
                if on_reject:
                    on_reject(repo, str(error))
                continue

            count = len(selected)
            if count < filters.min_files or (filters.max_files and count > filters.max_files):
                if on_reject:
                    on_reject(repo, f"{count} source files outside the budget")
                continue

            index, repository_id = _next_repository_id(hit["name"], index, taken)
            taken.add(repository_id)
            candidate = RepoCandidate(
                repo=repo,
                id=repository_id,
                ref=commit,
                default_branch=hit["default_branch"],
                stars=hit.get("stargazers_count", 0),
                open_issues=hit.get("open_issues_count", 0),
                license=(hit.get("license") or {}).get("spdx_id"),
                size_kb=hit.get("size", 0),
                source_files=count,
                languages=tuple(language_priority(entry.path for entry in selected)),
            )
            candidates.append(candidate)
            if on_candidate:
                on_candidate(candidate)
    return candidates


def _reject_reason(hit: dict[str, Any], min_open_issues: int) -> str | None:
    """Cheap local checks on a search hit, before spending a trees request on it."""
    if hit.get("fork"):
        return "fork"
    if hit.get("archived"):
        return "archived"
    if hit.get("is_template"):
        return "template"
    if not hit.get("has_issues", True):
        return "issues disabled"
    open_issues = hit.get("open_issues_count", 0)
    if open_issues < min_open_issues:
        return f"{open_issues} open issues (min {min_open_issues})"
    return None


_SLUG_UNSAFE = re.compile(r"[^a-z0-9]+")


def _slugify(name: str) -> str:
    return _SLUG_UNSAFE.sub("_", name.lower()).strip("_") or "repo"


def _next_repository_id(name: str, index: int, taken: set[str]) -> tuple[int, str]:
    """Allocate the next free ``repo_<NNN>_<slug>`` id."""
    slug = _slugify(name)
    while True:
        repository_id = f"repo_{index:03d}_{slug}"
        index += 1
        if repository_id not in taken:
            return index, repository_id


def next_dataset_index(dest_root: Path) -> int:
    """First free ``repo_<NNN>`` index in an existing dataset directory."""
    dest_root = Path(dest_root)
    if not dest_root.exists():
        return 1
    indices = [
        int(match.group(1))
        for item in dest_root.iterdir()
        if item.is_dir() and (match := re.match(r"repo_(\d+)_", item.name))
    ]
    return max(indices, default=0) + 1


def existing_repository_ids(dest_root: Path) -> list[str]:
    """Repository ids already present in the dataset directory."""
    dest_root = Path(dest_root)
    if not dest_root.exists():
        return []
    return sorted(item.name for item in dest_root.iterdir() if item.is_dir())


# --------------------------------------------------------------------------- #
# Manifest
# --------------------------------------------------------------------------- #
def build_manifest(candidates: Iterable[RepoCandidate]) -> dict[str, Any]:
    """Build the manifest mapping written by ``discover`` and read by ``fetch``.

    ``stars`` / ``source_files`` / ``license`` are informational: they are there for the
    human curating the list and are ignored by :func:`load_manifest`.
    """
    return {
        "version": 1,
        "repositories": [
            {
                "id": candidate.id,
                "repo": candidate.repo,
                "ref": candidate.ref,
                "stars": candidate.stars,
                "open_issues": candidate.open_issues,
                "license": candidate.license,
                "source_files": candidate.source_files,
                "languages": list(candidate.languages),
            }
            for candidate in candidates
        ],
    }


def load_manifest(path: Path) -> list[RepoSpec]:
    """Read a manifest into :class:`RepoSpec` entries.

    Only ``repo``, ``id``, ``ref`` and ``subdir`` are meaningful; the informational keys
    written by ``discover`` are ignored, so a hand-edited manifest works too.
    """
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("repositories"), list):
        raise ValueError(f"{path}: manifest must contain a 'repositories' list")

    specs: list[RepoSpec] = []
    for position, entry in enumerate(raw["repositories"], start=1):
        if not isinstance(entry, dict) or "repo" not in entry:
            raise ValueError(f"{path}: entry {position} must be a mapping with a 'repo' key")
        repo = str(entry["repo"]).strip().removeprefix("https://github.com/").strip("/")
        if repo.count("/") != 1:
            raise ValueError(f"{path}: entry {position}: 'repo' must be 'owner/name', got {repo!r}")
        name = repo.split("/", 1)[1]
        specs.append(
            RepoSpec(
                repo=repo,
                id=str(entry.get("id") or f"repo_{position:03d}_{_slugify(name)}"),
                ref=str(entry["ref"]) if entry.get("ref") else None,
                subdir=str(entry["subdir"]) if entry.get("subdir") else None,
            )
        )
    return specs
