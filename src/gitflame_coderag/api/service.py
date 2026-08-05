"""DB-backed implementation of the Agent Engine search contract."""

from __future__ import annotations

import fnmatch
import logging
from collections.abc import Callable
from pathlib import PurePosixPath
from typing import Protocol

from sqlalchemy import Engine

from gitflame_coderag.api.models import SearchRequest, SearchResult
from gitflame_coderag.api.settings import ApiSettings
from gitflame_coderag.embeddings import embed_query
from gitflame_coderag.pipelines.retrieve_issue import rank_issue_candidates
from gitflame_coderag.retrieval.selection import select_context_results
from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ExperimentConfig,
    Issue,
    RepositoryBundle,
)
from gitflame_coderag.storage.database import ping_database

logger = logging.getLogger(__name__)


class SearchBackend(Protocol):
    def ready(self) -> bool: ...

    def search(self, request: SearchRequest) -> list[SearchResult]: ...


class RepositoryReader(Protocol):
    @property
    def engine(self) -> Engine: ...

    def load_repository_bundle(
        self,
        repository_id: str,
        revision: str,
        *,
        embedding_model: str | None = None,
    ) -> RepositoryBundle: ...

    def load_latest_repository_revision(self, repository_id: str) -> str | None: ...


class DatabaseSearchBackend:
    def __init__(
        self,
        repository: RepositoryReader,
        settings: ApiSettings,
        *,
        embed_query_fn: Callable[..., list[float]] = embed_query,
    ) -> None:
        self.repository = repository
        self.settings = settings
        self.embed_query_fn = embed_query_fn

    def ready(self) -> bool:
        with self.repository.engine.connect() as connection:
            return ping_database(connection)

    def search(self, request: SearchRequest) -> list[SearchResult]:
        filters = request.filters
        revision = (
            filters.commit_sha
            or filters.revision
            or self.repository.load_latest_repository_revision(filters.repository_id)
        )
        if revision is None:
            return []

        bundle = self.repository.load_repository_bundle(
            filters.repository_id,
            revision,
            embedding_model=self.settings.embedding_model if self.settings.use_dense else None,
        )
        chunks = [
            chunk
            for chunk in bundle.chunks
            if _path_is_allowed(chunk.path, filters.include, filters.exclude)
        ]
        if not chunks:
            return []

        allowed_chunk_ids = {chunk.id for chunk in chunks}
        metadata = {
            chunk_id: value
            for chunk_id, value in bundle.metadata.items()
            if chunk_id in allowed_chunk_ids
        }
        embeddings = [
            value for value in bundle.embeddings if value.chunk_id in allowed_chunk_ids
        ]

        dense_enabled, query_vector = self._prepare_dense_query(request.query, embeddings)
        candidate_top_k = min(
            500,
            max(request.top_k, self.settings.candidate_top_k),
        )
        config = ExperimentConfig(
            name="http-search",
            use_bm25=True,
            use_dense=dense_enabled,
            use_ast=False,
            use_rrf=dense_enabled,
            use_reranker=False,
            bm25_top_k=candidate_top_k,
            dense_top_k=candidate_top_k,
            ast_top_k=candidate_top_k,
            rrf_top_k=candidate_top_k,
            reranker_top_k=candidate_top_k,
            final_top_k=candidate_top_k,
            embedding_model=self.settings.embedding_model,
        )
        ranked = rank_issue_candidates(
            issue=Issue(
                id="http-search",
                repository_id=filters.repository_id,
                title=request.query,
            ),
            chunks=chunks,
            metadata_by_chunk_id=metadata,
            config=config,
            embeddings=embeddings if dense_enabled else None,
            query_vector=query_vector,
            top_k=candidate_top_k,
        )

        chunks_by_id = {chunk.id: chunk for chunk in chunks}
        selected = select_context_results(
            ranked,
            chunks_by_id,
            max_chunks=request.top_k,
            min_relevance_score=self.settings.min_relevance_score,
            max_files=self.settings.max_context_files,
            max_chunks_per_file=self.settings.max_chunks_per_file,
            max_tokens=self.settings.max_context_tokens,
            deduplicate_overlaps=self.settings.deduplicate_overlaps,
            overlap_threshold=self.settings.overlap_threshold,
        )
        normalized_scores = _normalize_scores([item.score for item in selected.results])
        return [
            SearchResult(
                path=chunks_by_id[item.chunk_id].path,
                start_line=chunks_by_id[item.chunk_id].start_line,
                end_line=chunks_by_id[item.chunk_id].end_line,
                score=score,
                content=chunks_by_id[item.chunk_id].content[:50_000],
            )
            for item, score in zip(selected.results, normalized_scores, strict=True)
        ]

    def _prepare_dense_query(
        self,
        query: str,
        embeddings: list[ChunkEmbedding],
    ) -> tuple[bool, list[float] | None]:
        if not self.settings.use_dense or not embeddings:
            return False, None
        try:
            return True, self.embed_query_fn(query, model_name=self.settings.embedding_model)
        except Exception:
            logger.exception("Dense query embedding failed; falling back to BM25")
            return False, None


def _matches(path: str, pattern: str) -> bool:
    normalized = pattern.replace("\\", "/").removeprefix("./")
    if normalized in {"**", "**/*", "*"}:
        return True
    return fnmatch.fnmatchcase(path, normalized) or PurePosixPath(path).match(normalized)


def _path_is_allowed(path: str, include: list[str], exclude: list[str]) -> bool:
    included = not include or any(_matches(path, pattern) for pattern in include)
    return included and not any(_matches(path, pattern) for pattern in exclude)


def _normalize_scores(scores: list[float]) -> list[float]:
    """Return a stable per-query relevance score in the Agent Engine's [0, 1] range."""
    if not scores:
        return []
    maximum = max((score for score in scores if score > 0), default=0.0)
    if maximum == 0:
        return [0.0 for _ in scores]
    return [min(1.0, max(0.0, score / maximum)) for score in scores]
