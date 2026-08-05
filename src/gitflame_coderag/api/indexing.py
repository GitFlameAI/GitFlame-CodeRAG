"""Synchronous repository indexing used as a barrier before AI work starts."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Protocol

import yaml

from gitflame_coderag.api.models import IndexRequest, IndexResponse, IndexStatusResponse
from gitflame_coderag.api.settings import ApiSettings
from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.config import parse_ai_config
from gitflame_coderag.embeddings import (
    build_embedding_text,
    embed_chunks,
    extract_keywords_from_chunk,
)
from gitflame_coderag.ingestion import build_file_metadata, filter_files_by_config
from gitflame_coderag.retrieval.bm25 import build_bm25_text
from gitflame_coderag.schemas import (
    ChunkSearchTexts,
    Repository,
    RepositoryFile,
)
from gitflame_coderag.storage.repository import CodeRAGRepository


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

    def index(self, request: IndexRequest) -> IndexResponse:
        lock = self._repository_lock(request.repository_id)
        with lock:
            current = self.status(request.repository_id, request.commit_sha)
            if current.status == "indexed" and not request.force:
                return IndexResponse(**current.model_dump())

            config = _parse_configuration(request.configuration_yaml)
            seen_paths: set[str] = set()
            files: list[RepositoryFile] = []
            for item in request.files:
                if item.path in seen_paths:
                    raise ValueError(f"duplicate repository path: {item.path}")
                seen_paths.add(item.path)
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
            chunks = build_chunks(selected_files, config)
            if not chunks:
                raise ValueError("repository does not contain indexable text chunks")

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
            embeddings = (
                embed_chunks(
                    chunks,
                    metadata,
                    model_name=self.settings.embedding_model,
                    batch_size=config.embeddings.batch_size,
                    normalize_vectors=config.embeddings.normalize_vectors,
                )
                if self.settings.use_dense
                else []
            )
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
