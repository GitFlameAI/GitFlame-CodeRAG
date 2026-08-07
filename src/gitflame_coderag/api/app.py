"""FastAPI entry point for the CodeRAG service."""

from __future__ import annotations

import asyncio
import logging
import secrets
import threading

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Query, Request, status
from fastapi.concurrency import run_in_threadpool

from gitflame_coderag.api.indexing import (
    DatabaseIndexBackend,
    IndexBackend,
    IndexingCancelledError,
)
from gitflame_coderag.api.logging_config import setup_logging
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
    setup_logging("rag-service")
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
        payload: IndexRequest,
        http_request: Request,
        authorization: str | None = Header(default=None),
    ) -> IndexResponse:
        _authorize(authorization, resolved_settings.api_key)
        cancellation_event = threading.Event()

        def run_index() -> IndexResponse:
            if isinstance(resolved_index_backend, DatabaseIndexBackend):
                return resolved_index_backend.index(payload, cancellation_event)
            return resolved_index_backend.index(payload)

        task = asyncio.create_task(run_in_threadpool(run_index))
        try:
            while True:
                try:
                    return await asyncio.wait_for(asyncio.shield(task), timeout=0.25)
                except TimeoutError:
                    if await http_request.is_disconnected():
                        cancellation_event.set()
                        logger.warning(
                            "rag_index_cancelled repository_id=%s reason=client_disconnected",
                            payload.repository_id,
                        )
                        raise HTTPException(
                            status_code=499,
                            detail="repository indexing client disconnected",
                        )
        except IndexingCancelledError as exc:
            raise HTTPException(status_code=499, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception(
                "rag_index_failed repository_id=%s", payload.repository_id
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="repository indexing failed",
            ) from exc
        finally:
            cancellation_event.set()

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
