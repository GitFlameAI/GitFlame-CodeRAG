"""Synchronous repository indexing used as a barrier before AI work starts."""

from __future__ import annotations

import logging
import threading
from time import monotonic
from pathlib import Path
from typing import Protocol

import yaml

from gitflame_coderag.api.models import IndexRequest, IndexResponse, IndexStatusResponse
from gitflame_coderag.api.settings import ApiSettings
from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.config import parse_ai_config
from gitflame_coderag.embeddings import (
    EmbeddingCancelledError,
    build_embedding_text,
    embed_chunks,
    extract_keywords_from_chunk,
)
from gitflame_coderag.ingestion import build_file_metadata, filter_files_by_config
from gitflame_coderag.ingestion.files import is_indexable_text_file
from gitflame_coderag.retrieval.bm25 import build_bm25_text
from gitflame_coderag.schemas import (
    ChunkSearchTexts,
    Repository,
    RepositoryFile,
)
from gitflame_coderag.storage.repository import CodeRAGRepository

logger = logging.getLogger(__name__)


class IndexingCancelledError(RuntimeError):
    """Raised cooperatively after the indexing client disconnects or times out."""


class IndexBackend(Protocol):
    def status(self, repository_id: str, commit_sha: str) -> IndexStatusResponse: ...

    def index(self, request: IndexRequest) -> IndexResponse: ...


class DatabaseIndexBackend:
    """Build and atomically persist one active revision per repository."""

    def __init__(self, repository: CodeRAGRepository, settings: ApiSettings) -> None:
        self.repository = repository
        self.settings = settings
        self._locks_guard = threading.Lock()
        self._locks: dict[str, threading.Lock] = {}

    def status(self, repository_id: str, commit_sha: str) -> IndexStatusResponse:
        ready, files, chunks, embeddings = self.repository.repository_index_status(
            repository_id,
            commit_sha,
            embedding_model=self.settings.embedding_model if self.settings.use_dense else None,
        )
        return IndexStatusResponse(
            repository_id=repository_id,
            commit_sha=commit_sha,
            status="indexed" if ready else "missing",
            file_count=files,
            chunk_count=chunks,
            embedding_count=embeddings,
        )

    def index(
        self,
        request: IndexRequest,
        cancellation_event: threading.Event | None = None,
    ) -> IndexResponse:
        started = monotonic()

        def ensure_active() -> None:
            if cancellation_event is not None and cancellation_event.is_set():
                raise IndexingCancelledError("repository indexing was cancelled")

        def log_stage(stage: str, **fields: object) -> None:
            logger.info(
                "rag_index_stage",
                extra={
                    "event": "rag_index_stage",
                    "repository_id": request.repository_id,
                    "stage": stage,
                    "elapsed_ms": int((monotonic() - started) * 1000),
                    **fields,
                },
            )

        lock = self._repository_lock(request.repository_id)
        with lock:
            ensure_active()
            current = self.status(request.repository_id, request.commit_sha)
            if current.status == "indexed" and not request.force:
                return IndexResponse(**current.model_dump())

            log_stage("started", received_files=len(request.files))
            config = _parse_configuration(request.configuration_yaml)
            seen_paths: set[str] = set()
            files: list[RepositoryFile] = []
            skipped_binary = 0
            skipped_oversized = 0
            payload_bytes = 0
            for item in request.files:
                ensure_active()
                if item.path in seen_paths:
                    raise ValueError(f"duplicate repository path: {item.path}")
                seen_paths.add(item.path)
                if not is_indexable_text_file(item.path, item.content):
                    skipped_binary += 1
                    continue
                content_bytes = len(item.content.encode("utf-8"))
                if content_bytes > self.settings.max_index_file_bytes:
                    skipped_oversized += 1
                    continue
                payload_bytes += content_bytes
                if payload_bytes > self.settings.max_index_payload_bytes:
                    raise ValueError(
                        "repository index payload exceeds "
                        f"{self.settings.max_index_payload_bytes} bytes"
                    )
                files.append(
                    RepositoryFile(
                        metadata=build_file_metadata(
                            Path(item.path),
                            item.content,
                            request.repository_id,
                            request.commit_sha,
                            relative_path=item.path,
                        ),
                        raw_content=item.content,
                    )
                )

            selected_files = filter_files_by_config(files, config)
            if not selected_files:
                raise ValueError("repository configuration excluded every indexable file")
            log_stage(
                "files_selected",
                selected_files=len(selected_files),
                skipped_binary=skipped_binary,
                skipped_oversized=skipped_oversized,
                payload_bytes=payload_bytes,
            )
            ensure_active()
            chunks = build_chunks(selected_files, config)
            if not chunks:
                raise ValueError("repository does not contain indexable text chunks")
            log_stage("chunks_built", chunks=len(chunks))

            ensure_active()
            metadata = {
                chunk.id: extract_structural_metadata(chunk) for chunk in chunks
            }
            keywords = {
                chunk.id: extract_keywords_from_chunk(chunk) for chunk in chunks
            }
            search_texts = {
                chunk.id: ChunkSearchTexts(
                    chunk_id=chunk.id,
                    bm25_text=build_bm25_text(chunk, metadata[chunk.id]),
                    embedding_text=build_embedding_text(chunk, metadata[chunk.id]),
                )
                for chunk in chunks
            }
            try:
                embeddings = (
                    embed_chunks(
                        chunks,
                        metadata,
                        model_name=self.settings.embedding_model,
                        batch_size=config.embeddings.batch_size,
                        normalize_vectors=config.embeddings.normalize_vectors,
                        progress_callback=lambda done, total: log_stage(
                            "embeddings_progress", done=done, total=total
                        ),
                        cancellation_callback=lambda: cancellation_event is not None
                        and cancellation_event.is_set(),
                    )
                    if self.settings.use_dense
                    else []
                )
            except EmbeddingCancelledError as exc:
                raise IndexingCancelledError(str(exc)) from exc
            ensure_active()
            log_stage("embeddings_built", embeddings=len(embeddings))
            self.repository.replace_repository_index(
                Repository(
                    id=request.repository_id,
                    name=request.repository_name or request.repository_id.rsplit("/", 1)[-1],
                    source=request.source or "gitflame",
                    revision=request.commit_sha,
                    root_path=request.source or "",
                ),
                selected_files,
                chunks,
                metadata,
                keywords,
                search_texts,
                embeddings,
            )
            log_stage("completed", files=len(selected_files), chunks=len(chunks))
            return IndexResponse(
                repository_id=request.repository_id,
                commit_sha=request.commit_sha,
                status="indexed",
                file_count=len(selected_files),
                chunk_count=len(chunks),
                embedding_count=len(embeddings),
            )

    def _repository_lock(self, repository_id: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(repository_id, threading.Lock())


def _parse_configuration(raw: str):
    if not raw.strip():
        return parse_ai_config({})
    document = yaml.safe_load(raw)
    if not isinstance(document, dict):
        raise ValueError("repository configuration must contain a YAML mapping")
    return parse_ai_config(document)
