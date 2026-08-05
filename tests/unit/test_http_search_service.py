from gitflame_coderag.api.models import SearchFilters, SearchRequest
from gitflame_coderag.api.service import DatabaseSearchBackend, _normalize_scores
from gitflame_coderag.api.settings import ApiSettings
from gitflame_coderag.schemas import CodeChunk, RepositoryBundle, StructuralMetadata


def _chunk(
    chunk_id: str,
    path: str,
    content: str,
    *,
    start_line: int = 1,
    end_line: int = 4,
) -> CodeChunk:
    return CodeChunk(
        id=chunk_id,
        repository_id="owner/repository",
        file_id=f"file-{chunk_id}",
        path=path,
        language="python",
        chunk_type="ast",
        node_type="function_definition",
        start_line=start_line,
        end_line=end_line,
        content=content,
        content_hash=f"hash-{chunk_id}",
        token_count=20,
    )


class FakeRepository:
    def __init__(self, bundle: RepositoryBundle, *, latest_revision: str | None = "abc123") -> None:
        self.bundle = bundle
        self.latest_revision = latest_revision
        self.requested_revision: str | None = None

    def load_latest_repository_revision(self, repository_id: str) -> str | None:
        assert repository_id == "owner/repository"
        return self.latest_revision

    def load_repository_bundle(
        self,
        repository_id: str,
        revision: str,
        *,
        embedding_model: str | None = None,
    ) -> RepositoryBundle:
        assert repository_id == "owner/repository"
        assert embedding_model is None
        self.requested_revision = revision
        return self.bundle


def _bundle() -> RepositoryBundle:
    chunks = [
        _chunk("auth", "src/auth.py", "def authenticate(token): return verify(token)"),
        _chunk("test", "tests/test_auth.py", "def test_authenticate(): assert authenticate('x')"),
        _chunk("cache", "src/cache.py", "def store_cache(value): return value"),
    ]
    return RepositoryBundle(
        repository_id="owner/repository",
        revision="abc123",
        chunks=chunks,
        metadata={chunk.id: StructuralMetadata(chunk_id=chunk.id) for chunk in chunks},
        embeddings=[],
    )


def _settings(**overrides: object) -> ApiSettings:
    values = {
        "database_url": "postgresql+psycopg://unused",
        "use_dense": False,
        "max_context_files": 20,
        "max_chunks_per_file": 3,
        "max_context_tokens": 12_000,
    }
    values.update(overrides)
    return ApiSettings(**values)  # type: ignore[arg-type]


def test_search_respects_revision_path_filters_and_top_k() -> None:
    repository = FakeRepository(_bundle())
    backend = DatabaseSearchBackend(repository, _settings())  # type: ignore[arg-type]
    request = SearchRequest(
        query="authenticate token",
        top_k=1,
        filters=SearchFilters(
            repository_id="owner/repository",
            commit_sha="abc123",
            include=["src/**"],
            exclude=["src/cache.py"],
        ),
    )

    results = backend.search(request)

    assert repository.requested_revision == "abc123"
    assert len(results) == 1
    assert results[0].path == "src/auth.py"
    assert results[0].score == 1.0
    assert 0 <= results[0].score <= 1


def test_search_uses_latest_indexed_revision_when_commit_is_missing() -> None:
    repository = FakeRepository(_bundle(), latest_revision="latest-indexed")
    backend = DatabaseSearchBackend(repository, _settings())  # type: ignore[arg-type]

    backend.search(
        SearchRequest(
            query="authenticate",
            filters=SearchFilters(repository_id="owner/repository"),
        )
    )

    assert repository.requested_revision == "latest-indexed"


def test_search_returns_empty_when_repository_has_no_indexed_revision() -> None:
    repository = FakeRepository(_bundle(), latest_revision=None)
    backend = DatabaseSearchBackend(repository, _settings())  # type: ignore[arg-type]

    results = backend.search(
        SearchRequest(
            query="authenticate",
            filters=SearchFilters(repository_id="owner/repository"),
        )
    )

    assert results == []
    assert repository.requested_revision is None


def test_score_normalization_clamps_negative_values() -> None:
    assert _normalize_scores([4.0, 2.0, -1.0]) == [1.0, 0.5, 0.0]
    assert _normalize_scores([-1.0, 0.0]) == [0.0, 0.0]
