"""Tests for GitHub dataset collection (no network: fake client + in-memory tarball)."""

from __future__ import annotations

import io
import re
import tarfile
import urllib.error
from email.message import Message
from pathlib import Path
from typing import Any

import pytest
import yaml

from gitflame_coderag.config.loader import parse_ai_config
from gitflame_coderag.ingestion.files import filter_files_by_config, load_repository_files
from gitflame_coderag.ingestion.github import (
    FileFilters,
    GitHubClient,
    GitHubError,
    GitHubRateLimitError,
    RepoSpec,
    TreeEntry,
    build_manifest,
    build_repo_config,
    discover_repositories,
    extract_files,
    fetch_repository,
    include_patterns,
    language_priority,
    load_manifest,
    next_dataset_index,
    select_files,
)

COMMIT = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"


# --------------------------------------------------------------------------- #
# Fakes
# --------------------------------------------------------------------------- #
def make_tarball(files: dict[str, bytes], root: str = "owner-name-a1b2c3d") -> bytes:
    """Build a GitHub-style tarball: every member under an ``owner-name-sha/`` root."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for path, payload in files.items():
            info = tarfile.TarInfo(f"{root}/{path}")
            info.size = len(payload)
            tar.addfile(info, io.BytesIO(payload))
    return buffer.getvalue()


class FakeClient:
    """Stand-in for :class:`GitHubClient` serving canned metadata, trees and tarballs."""

    def __init__(
        self,
        repos: dict[str, dict[str, Any]],
        *,
        search_hits: list[dict[str, Any]] | None = None,
    ) -> None:
        self.repos = repos
        self.search_hits = search_hits or []
        self.paths: list[str] = []

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        self.paths.append(path)
        if path == "/search/repositories":
            page = int((params or {}).get("page", 1))
            language = _query_language((params or {}).get("q", ""))
            hits = [hit for hit in self.search_hits if hit.get("language") == language]
            return {"total_count": len(hits), "items": hits if page == 1 else []}

        match = re.fullmatch(r"/repos/([^/]+/[^/]+)(?:/(commits|git/trees)/(.+))?", path)
        if not match:
            raise AssertionError(f"unexpected path: {path}")
        repo, kind, _ = match.groups()
        if repo not in self.repos:
            raise GitHubError(f"GET {path} -> 404 Not Found")
        entry = self.repos[repo]
        if kind is None:
            return entry["metadata"]
        if kind == "commits":
            return {"sha": entry.get("commit", COMMIT)}
        return {
            "truncated": entry.get("truncated", False),
            "tree": [
                {"path": path, "type": "blob", "size": size}
                for path, size in entry["tree"].items()
            ],
        }

    def get_bytes(self, path: str, params: dict[str, Any] | None = None) -> bytes:
        self.paths.append(path)
        repo = path.split("/tarball/")[0].removeprefix("/repos/")
        return make_tarball(self.repos[repo]["files"])


def _query_language(query: str) -> str:
    match = re.search(r"language:(\S+)", query)
    return match.group(1) if match else ""


def repo_entry(
    full_name: str,
    files: dict[str, bytes],
    *,
    stars: int = 500,
    license_id: str | None = "MIT",
) -> dict[str, Any]:
    owner, name = full_name.split("/")
    return {
        "metadata": {
            "name": name,
            "full_name": full_name,
            "html_url": f"https://github.com/{full_name}",
            "default_branch": "main",
            "stargazers_count": stars,
            "license": {"spdx_id": license_id} if license_id else None,
        },
        "commit": COMMIT,
        "tree": {path: len(payload) for path, payload in files.items()},
        "files": files,
    }


def search_hit(full_name: str, language: str, **overrides: Any) -> dict[str, Any]:
    hit = {
        "full_name": full_name,
        "name": full_name.split("/")[1],
        "language": language,
        "default_branch": "main",
        "stargazers_count": 900,
        "open_issues_count": 12,
        "size": 400,
        "license": {"spdx_id": "MIT"},
        "fork": False,
        "archived": False,
        "is_template": False,
        "has_issues": True,
    }
    hit.update(overrides)
    return hit


# --------------------------------------------------------------------------- #
# select_files
# --------------------------------------------------------------------------- #
def test_select_files_keeps_source_and_drops_the_rest() -> None:
    entries = [
        TreeEntry("app/main.py", 800),
        TreeEntry("app/util.go", 400),
        TreeEntry("README.md", 200),  # Not a source extension.
        TreeEntry("app/logo.png", 900),  # Not a source extension.
        TreeEntry("web/node_modules/left-pad/index.js", 100),  # Vendored, nested.
        TreeEntry("web/app.min.js", 100),  # Minified.
        TreeEntry("app/huge.py", 500_000),  # Over the size cap.
        TreeEntry(".devcontainer/on-create.sh", 100),  # CI tooling, not the code under test.
        TreeEntry("tools/.github/scripts/release.py", 100),  # Hidden dir at any depth.
    ]

    selected = select_files(entries, FileFilters(max_file_bytes=200_000))

    assert [entry.path for entry in selected] == ["app/main.py", "app/util.go"]


def test_select_files_sorts_shallow_paths_first() -> None:
    entries = [TreeEntry("a/b/c/deep.py", 10), TreeEntry("root.py", 10), TreeEntry("a/mid.py", 10)]

    assert [entry.path for entry in select_files(entries, FileFilters())] == [
        "root.py",
        "a/mid.py",
        "a/b/c/deep.py",
    ]


@pytest.mark.parametrize(
    ("path", "is_test"),
    [
        ("tests/test_api.py", True),
        ("app/api_test.go", True),
        ("src/api.spec.ts", True),
        ("app/api.py", False),
    ],
)
def test_select_files_can_exclude_tests(path: str, is_test: bool) -> None:
    entries = [TreeEntry(path, 100)]

    kept = select_files(entries, FileFilters(include_tests=False))

    assert (kept == []) is is_test


def test_select_files_restricts_to_subdir() -> None:
    entries = [TreeEntry("packages/core/index.ts", 10), TreeEntry("packages/cli/main.ts", 10)]

    selected = select_files(entries, FileFilters(), subdir="packages/core")

    assert [entry.path for entry in selected] == ["packages/core/index.ts"]


# --------------------------------------------------------------------------- #
# extract_files
# --------------------------------------------------------------------------- #
def test_extract_files_writes_only_selected_paths(tmp_path: Path) -> None:
    archive = make_tarball(
        {
            "app/main.py": b"print('hi')\n",
            "app/skip.py": b"unused\n",
            "app/logo.png": b"\x89PNG\r\n\x1a\n\xff\xfe",
        }
    )

    written = extract_files(archive, ["app/main.py", "app/logo.png"], tmp_path)

    assert written == ["app/main.py"]  # The png is requested but not decodable as text.
    assert (tmp_path / "app" / "main.py").read_bytes() == b"print('hi')\n"
    assert not (tmp_path / "app" / "skip.py").exists()
    assert not (tmp_path / "app" / "logo.png").exists()


def test_extract_files_skips_binary_content(tmp_path: Path) -> None:
    archive = make_tarball({"app/fake.py": b"\xff\xfe\x00binary"})

    written = extract_files(archive, ["app/fake.py"], tmp_path)

    assert written == []
    assert not (tmp_path / "app" / "fake.py").exists()


def test_extract_files_reroots_subdir(tmp_path: Path) -> None:
    archive = make_tarball({"packages/core/index.ts": b"export const a = 1\n"})

    written = extract_files(archive, ["packages/core/index.ts"], tmp_path, subdir="packages/core")

    assert written == ["index.ts"]
    assert (tmp_path / "index.ts").exists()


def test_extract_files_ignores_path_traversal(tmp_path: Path) -> None:
    dest = tmp_path / "code"
    dest.mkdir()
    archive = make_tarball({"../../evil.py": b"pwned\n"})

    written = extract_files(archive, ["../../evil.py"], dest)

    assert written == []
    assert not (tmp_path.parent / "evil.py").exists()


# --------------------------------------------------------------------------- #
# repo.yml
# --------------------------------------------------------------------------- #
def test_language_priority_orders_by_frequency() -> None:
    paths = ["a.py", "b.py", "c.go", "d.md"]

    assert language_priority(paths) == ["python", "go"]


def test_include_patterns_covers_directories_and_root_files() -> None:
    assert include_patterns(["src/a.py", "src/b/c.py", "main.py"]) == ["*.py", "src/**"]


def test_generated_config_selects_exactly_the_fetched_files(tmp_path: Path) -> None:
    """The include/exclude written into repo.yml must round-trip through ingestion."""
    paths = ["app/main.py", "app/api/routes.py", "tests/test_main.py", "setup.py"]
    for path in paths:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x = 1\n", encoding="utf-8")
    metadata = repo_entry("owner/name", {})["metadata"]

    config = build_repo_config(metadata, COMMIT, paths)
    parsed = parse_ai_config(yaml.safe_load(yaml.safe_dump(config)))
    files = filter_files_by_config(load_repository_files(tmp_path, "repo_001", COMMIT), parsed)

    assert sorted(file.metadata.path for file in files) == sorted(paths)


def test_build_repo_config_records_provenance() -> None:
    metadata = repo_entry("encode/httpx", {}, stars=13000, license_id="BSD-3-Clause")["metadata"]

    config = build_repo_config(metadata, COMMIT, ["httpx/api.py"], subdir="httpx")

    assert config["repository"] == {
        "name": "httpx",
        "full_name": "encode/httpx",
        "url": "https://github.com/encode/httpx",
        "default_branch": "main",
        "revision": COMMIT,
        "license": "BSD-3-Clause",
        "stars": 13000,
        "language_priority": ["python"],
        "subdir": "httpx",
    }
    assert config["issues"]["source"] == "github"


# --------------------------------------------------------------------------- #
# fetch_repository
# --------------------------------------------------------------------------- #
@pytest.fixture
def client() -> FakeClient:
    return FakeClient(
        {
            "encode/httpx": repo_entry(
                "encode/httpx",
                {
                    "httpx/api.py": b"def get(url):\n    return url\n",
                    "httpx/_client.py": b"class Client:\n    pass\n",
                    "tests/test_api.py": b"def test_get():\n    assert True\n",
                    "README.md": b"# httpx\n",
                },
            )
        }
    )


def test_fetch_repository_writes_code_and_config(client: FakeClient, tmp_path: Path) -> None:
    spec = RepoSpec(repo="encode/httpx", id="repo_019_httpx")

    result = fetch_repository(client, spec, tmp_path)

    assert result.skipped is None
    assert result.commit == COMMIT
    assert result.files == ["httpx/_client.py", "httpx/api.py", "tests/test_api.py"]
    repo_dir = tmp_path / "repo_019_httpx"
    api = (repo_dir / "code" / "httpx" / "api.py").read_text(encoding="utf-8")
    assert api.startswith("def get")
    assert not (repo_dir / "code" / "README.md").exists()  # Not a source extension.
    config = yaml.safe_load((repo_dir / "repo.yml").read_text(encoding="utf-8"))
    assert config["repository"]["revision"] == COMMIT
    assert config["repository"]["language_priority"] == ["python"]


def test_fetch_repository_never_touches_issues(client: FakeClient, tmp_path: Path) -> None:
    """issues.jsonl is authored by hand: it must survive a --force re-fetch."""
    spec = RepoSpec(repo="encode/httpx", id="repo_019_httpx")
    fetch_repository(client, spec, tmp_path)
    issues = tmp_path / "repo_019_httpx" / "issues.jsonl"
    issues.write_text('{"id": "i1", "title": "t"}\n', encoding="utf-8")
    stale = tmp_path / "repo_019_httpx" / "code" / "gone.py"
    stale.write_text("removed upstream\n", encoding="utf-8")

    result = fetch_repository(client, spec, tmp_path, force=True)

    assert result.has_issues is True
    assert issues.read_text(encoding="utf-8") == '{"id": "i1", "title": "t"}\n'
    assert not stale.exists()  # Refresh drops files that vanished upstream.


def test_fetch_repository_skips_existing_without_force(client: FakeClient, tmp_path: Path) -> None:
    spec = RepoSpec(repo="encode/httpx", id="repo_019_httpx")
    fetch_repository(client, spec, tmp_path)
    calls = len(client.paths)

    result = fetch_repository(client, spec, tmp_path)

    assert result.skipped is not None
    assert len(client.paths) == calls  # Nothing re-downloaded.


def test_fetch_repository_skips_over_budget(client: FakeClient, tmp_path: Path) -> None:
    spec = RepoSpec(repo="encode/httpx", id="repo_019_httpx")

    result = fetch_repository(client, spec, tmp_path, FileFilters(max_files=2, min_files=1))

    assert result.skipped == "3 source files exceed the max of 2"
    assert not (tmp_path / "repo_019_httpx" / "code").exists()


def test_fetch_repository_reports_missing_issues(client: FakeClient, tmp_path: Path) -> None:
    result = fetch_repository(client, RepoSpec(repo="encode/httpx", id="r"), tmp_path)

    assert result.has_issues is False


# --------------------------------------------------------------------------- #
# discover_repositories
# --------------------------------------------------------------------------- #
def test_discover_filters_by_real_file_count(tmp_path: Path) -> None:
    small = {f"src/mod_{index}.py": b"x = 1\n" for index in range(5)}
    huge = {f"src/mod_{index}.py": b"x = 1\n" for index in range(150)}
    client = FakeClient(
        {
            "owner/small": repo_entry("owner/small", small),
            "owner/huge": repo_entry("owner/huge", huge),
            "owner/go-lib": repo_entry("owner/go-lib", {"main.go": b"package main\n"}),
        },
        search_hits=[
            search_hit("owner/huge", "python"),
            search_hit("owner/small", "python"),
            search_hit("owner/go-lib", "go"),
        ],
    )
    rejected: list[tuple[str, str]] = []

    candidates = discover_repositories(
        client,
        languages=["python", "go"],
        filters=FileFilters(max_files=100, min_files=3),
        limit=10,
        on_reject=lambda repo, reason: rejected.append((repo, reason)),
    )

    assert [candidate.repo for candidate in candidates] == ["owner/small"]
    assert ("owner/huge", "150 source files outside the budget") in rejected
    assert ("owner/go-lib", "1 source files outside the budget") in rejected  # Below min_files.
    assert candidates[0].source_files == 5
    assert candidates[0].ref == COMMIT
    assert candidates[0].languages == ("python",)


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        ({"fork": True}, "fork"),
        ({"archived": True}, "archived"),
        ({"is_template": True}, "template"),
        ({"has_issues": False}, "issues disabled"),
        ({"open_issues_count": 1}, "1 open issues (min 5)"),
    ],
)
def test_discover_rejects_unusable_hits(overrides: dict[str, Any], reason: str) -> None:
    client = FakeClient(
        {"owner/repo": repo_entry("owner/repo", {"a.py": b"x = 1\n"})},
        search_hits=[search_hit("owner/repo", "python", **overrides)],
    )
    rejected: list[tuple[str, str]] = []

    candidates = discover_repositories(
        client,
        languages=["python"],
        min_open_issues=5,
        on_reject=lambda repo, why: rejected.append((repo, why)),
    )

    assert candidates == []
    assert rejected == [("owner/repo", reason)]
    assert client.paths == ["/search/repositories"]  # No trees request wasted on it.


def test_discover_allocates_ids_after_existing_dataset(tmp_path: Path) -> None:
    (tmp_path / "repo_001_fastapi_blog").mkdir()
    (tmp_path / "repo_018_ruby_rails_billing").mkdir()
    client = FakeClient(
        {"owner/httpx": repo_entry("owner/httpx", {f"a{i}.py": b"x = 1\n" for i in range(4)})},
        search_hits=[search_hit("owner/httpx", "python")],
    )

    candidates = discover_repositories(
        client,
        languages=["python"],
        existing_ids=[path.name for path in tmp_path.iterdir()],
        start_index=next_dataset_index(tmp_path),
    )

    assert [candidate.id for candidate in candidates] == ["repo_019_httpx"]


# --------------------------------------------------------------------------- #
# Manifest
# --------------------------------------------------------------------------- #
def test_manifest_round_trips(tmp_path: Path) -> None:
    client = FakeClient(
        {"owner/httpx": repo_entry("owner/httpx", {f"a{i}.py": b"x = 1\n" for i in range(4)})},
        search_hits=[search_hit("owner/httpx", "python")],
    )
    candidates = discover_repositories(client, languages=["python"])
    manifest = tmp_path / "github_repos.yml"
    manifest.write_text(yaml.safe_dump(build_manifest(candidates)), encoding="utf-8")

    specs = load_manifest(manifest)

    assert specs == [RepoSpec(repo="owner/httpx", id="repo_001_httpx", ref=COMMIT)]


def test_load_manifest_accepts_hand_written_entries(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "repositories": [
                    {"repo": "https://github.com/encode/httpx/", "id": "repo_020_httpx"},
                    {"repo": "lerna/lerna", "subdir": "packages/core"},
                ]
            }
        ),
        encoding="utf-8",
    )

    specs = load_manifest(manifest)

    assert specs[0] == RepoSpec(repo="encode/httpx", id="repo_020_httpx")
    assert specs[1] == RepoSpec(repo="lerna/lerna", id="repo_002_lerna", subdir="packages/core")


@pytest.mark.parametrize(
    "payload",
    [{"repositories": [{"id": "x"}]}, {"repositories": [{"repo": "no-owner"}]}, {"repos": []}],
)
def test_load_manifest_rejects_malformed(payload: dict[str, Any], tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(yaml.safe_dump(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        load_manifest(manifest)


# --------------------------------------------------------------------------- #
# Rate limiting
# --------------------------------------------------------------------------- #
def http_error(code: int, headers: dict[str, str]) -> urllib.error.HTTPError:
    message = Message()
    for key, value in headers.items():
        message[key] = value
    return urllib.error.HTTPError("https://api.github.com", code, "err", message, None)


def test_retry_delay_waits_out_the_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("gitflame_coderag.ingestion.github.time.time", lambda: 1000.0)
    client = GitHubClient(token="t", max_wait=300)

    error = http_error(403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "1060"})

    assert client._retry_delay(error, attempt=0) == pytest.approx(61.0)


def test_retry_delay_raises_when_reset_is_too_far(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("gitflame_coderag.ingestion.github.time.time", lambda: 1000.0)
    client = GitHubClient(token="t", max_wait=60)

    error = http_error(429, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "9999"})

    with pytest.raises(GitHubRateLimitError):
        client._retry_delay(error, attempt=0)


def test_client_tracks_the_remaining_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Progress reporting reads these counters during long runs."""

    class Response:
        headers = {"x-ratelimit-remaining": "4832", "x-ratelimit-reset": "1700000000"}

        def read(self) -> bytes:
            return b"{}"

        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

    monkeypatch.setattr(
        "gitflame_coderag.ingestion.github.urllib.request.urlopen",
        lambda request, timeout: Response(),
    )
    client = GitHubClient(token="t")

    client.get_json("/repos/owner/name")

    assert client.rate_limit_remaining == 4832
    assert client.rate_limit_reset == 1700000000.0
    assert client.requests_made == 1


def test_retry_delay_gives_up_on_client_errors() -> None:
    client = GitHubClient(token="t")

    assert client._retry_delay(http_error(404, {}), attempt=0) is None
    assert client._retry_delay(http_error(403, {}), attempt=0) is None  # Not a rate limit.
    assert client._retry_delay(http_error(502, {}), attempt=0) == pytest.approx(1.0)
