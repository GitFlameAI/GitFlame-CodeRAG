"""FastAPI entry point for the CodeRAG service."""

from __future__ import annotations

import logging
import secrets

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.concurrency import run_in_threadpool

from gitflame_coderag.api.indexing import DatabaseIndexBackend, IndexBackend
from gitflame_coderag.api.models import (
    HealthResponse,
    IndexRequest,
    IndexResponse,
    IndexStatusResponse,
    SearchRequest,
    SearchResponse,
)
from gitflame_coderag.api.service import DatabaseSearchBackend, SearchBackend
from gitflame_coderag.api.settings import ApiSettings
from gitflame_coderag.storage.database import create_engine_from_url
from gitflame_coderag.storage.repository import CodeRAGRepository

logger = logging.getLogger(__name__)


def create_app(
    *,
    settings: ApiSettings | None = None,
    backend: SearchBackend | None = None,
    index_backend: IndexBackend | None = None,
) -> FastAPI:
    resolved_settings = settings or ApiSettings.from_env()
    resolved_settings.validate()
    repository = CodeRAGRepository(create_engine_from_url(resolved_settings.database_url))
    resolved_backend = backend or DatabaseSearchBackend(repository, resolved_settings)
    resolved_index_backend = index_backend or DatabaseIndexBackend(repository, resolved_settings)
    application = FastAPI(
        title="GitFlame CodeRAG",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
    )

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        try:
            ready = await run_in_threadpool(resolved_backend.ready)
        except Exception as exc:
            logger.exception("CodeRAG search failed")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="database is unavailable",
            ) from exc
        if not ready:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="database is unavailable",
            )
        return HealthResponse(status="ok", database="ready")

    @application.post("/search", response_model=SearchResponse)
    async def search(
        request: SearchRequest,
        authorization: str | None = Header(default=None),
    ) -> SearchResponse:
        _authorize(authorization, resolved_settings.api_key)
        try:
            results = await run_in_threadpool(resolved_backend.search, request)
        except Exception as exc:
            logger.exception("CodeRAG index status failed")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="search backend is unavailable",
            ) from exc
        return SearchResponse(results=results)

    @application.get("/indexes/status", response_model=IndexStatusResponse)
    async def index_status(
        repository_id: str = Query(min_length=1, max_length=200),
        commit_sha: str = Query(min_length=1, max_length=200),
        authorization: str | None = Header(default=None),
    ) -> IndexStatusResponse:
        _authorize(authorization, resolved_settings.api_key)
        try:
            return await run_in_threadpool(
                resolved_index_backend.status,
                repository_id,
                commit_sha,
            )
        except Exception as exc:
            logger.exception("CodeRAG repository indexing failed")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="index status backend is unavailable",
            ) from exc

    @application.post("/indexes", response_model=IndexResponse)
    async def index_repository(
        request: IndexRequest,
        authorization: str | None = Header(default=None),
    ) -> IndexResponse:
        _authorize(authorization, resolved_settings.api_key)
        try:
            return await run_in_threadpool(resolved_index_backend.index, request)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="repository indexing failed",
            ) from exc

    return application


def _authorize(authorization: str | None, expected_api_key: str | None) -> None:
    if expected_api_key is None:
        return
    scheme, _, supplied_key = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(supplied_key, expected_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


app = create_app()


def run() -> None:
    settings = ApiSettings.from_env()
    uvicorn.run(
        "gitflame_coderag.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
