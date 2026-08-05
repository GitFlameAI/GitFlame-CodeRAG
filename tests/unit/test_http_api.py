from fastapi.testclient import TestClient

from gitflame_coderag.api.app import create_app
from gitflame_coderag.api.models import SearchRequest, SearchResult
from gitflame_coderag.api.settings import ApiSettings


class FakeBackend:
    def __init__(self, *, ready: bool = True, results: list[SearchResult] | None = None) -> None:
        self.is_ready = ready
        self.results = results or []
        self.last_request: SearchRequest | None = None

    def ready(self) -> bool:
        return self.is_ready

    def search(self, request: SearchRequest) -> list[SearchResult]:
        self.last_request = request
        return self.results


def _settings(*, api_key: str | None = None) -> ApiSettings:
    return ApiSettings(database_url="postgresql+psycopg://unused", api_key=api_key)


def _payload() -> dict[str, object]:
    return {
        "query": "find authentication handler",
        "top_k": 5,
        "filters": {
            "repository_id": "owner/repository",
            "commit_sha": "abc123",
            "include": ["src/**"],
            "exclude": ["**/test_*.py"],
        },
    }


def test_health_is_public_and_reports_database_readiness() -> None:
    client = TestClient(create_app(settings=_settings(api_key="secret"), backend=FakeBackend()))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ready", "version": "1.0.0"}


def test_health_returns_503_when_database_is_not_ready() -> None:
    client = TestClient(
        create_app(settings=_settings(), backend=FakeBackend(ready=False)),
        raise_server_exceptions=False,
    )

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"detail": "database is unavailable"}


def test_search_requires_configured_bearer_token() -> None:
    client = TestClient(create_app(settings=_settings(api_key="secret"), backend=FakeBackend()))

    missing = client.post("/search", json=_payload())
    invalid = client.post(
        "/search",
        json=_payload(),
        headers={"Authorization": "Bearer wrong"},
    )

    assert missing.status_code == 401
    assert invalid.status_code == 401


def test_search_returns_agent_engine_contract() -> None:
    backend = FakeBackend(
        results=[
            SearchResult(
                path="src/auth.py",
                start_line=10,
                end_line=20,
                score=0.91,
                content="def authenticate(): ...",
            )
        ]
    )
    client = TestClient(create_app(settings=_settings(api_key="secret"), backend=backend))

    response = client.post(
        "/search",
        json=_payload(),
        headers={"Authorization": "Bearer secret"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "path": "src/auth.py",
                "start_line": 10,
                "end_line": 20,
                "score": 0.91,
                "content": "def authenticate(): ...",
            }
        ]
    }
    assert backend.last_request is not None
    assert backend.last_request.filters.repository_id == "owner/repository"


def test_search_returns_empty_results_without_fake_evidence() -> None:
    client = TestClient(create_app(settings=_settings(), backend=FakeBackend()))

    response = client.post("/search", json=_payload())

    assert response.status_code == 200
    assert response.json() == {"results": []}


def test_search_rejects_blank_query_and_oversized_top_k() -> None:
    client = TestClient(create_app(settings=_settings(), backend=FakeBackend()))
    payload = _payload()
    payload["query"] = "   "
    payload["top_k"] = 51

    response = client.post("/search", json=payload)

    assert response.status_code == 422
