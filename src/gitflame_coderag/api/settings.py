"""Environment configuration for the CodeRAG HTTP process."""

from __future__ import annotations

import os
from dataclasses import dataclass

from gitflame_coderag.embeddings import DEFAULT_EMBEDDING_MODEL


def _optional_int(name: str, default: int | None) -> int | None:
    raw = os.getenv(name)
    return default if raw in (None, "") else int(raw)


def _optional_float(name: str, default: float | None) -> float | None:
    raw = os.getenv(name)
    return default if raw in (None, "") else float(raw)


def _boolean(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean")


@dataclass(frozen=True)
class ApiSettings:
    database_url: str
    api_key: str | None = None
    host: str = "0.0.0.0"
    port: int = 8004
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    use_dense: bool = True
    candidate_top_k: int = 50
    min_relevance_score: float | None = None
    max_context_files: int | None = 20
    max_chunks_per_file: int | None = 3
    max_context_tokens: int | None = 12_000
    deduplicate_overlaps: bool = True
    overlap_threshold: float = 0.8

    @classmethod
    def from_env(cls) -> ApiSettings:
        settings = cls(
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg://gitflame:gitflame@localhost:5432/gitflame_coderag",
            ),
            api_key=os.getenv("RAG_API_KEY") or None,
            host=os.getenv("RAG_HOST", "0.0.0.0"),
            port=int(os.getenv("RAG_PORT", "8004")),
            embedding_model=os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
            use_dense=_boolean("RAG_USE_DENSE", True),
            candidate_top_k=int(os.getenv("RAG_CANDIDATE_TOP_K", "50")),
            min_relevance_score=_optional_float("RAG_MIN_RELEVANCE_SCORE", None),
            max_context_files=_optional_int("RAG_MAX_CONTEXT_FILES", 20),
            max_chunks_per_file=_optional_int("RAG_MAX_CHUNKS_PER_FILE", 3),
            max_context_tokens=_optional_int("RAG_MAX_CONTEXT_TOKENS", 12_000),
            deduplicate_overlaps=_boolean("RAG_DEDUPLICATE_OVERLAPS", True),
            overlap_threshold=float(os.getenv("RAG_OVERLAP_THRESHOLD", "0.8")),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        for name, value in (
            ("port", self.port),
            ("candidate_top_k", self.candidate_top_k),
            ("max_context_files", self.max_context_files),
            ("max_chunks_per_file", self.max_chunks_per_file),
            ("max_context_tokens", self.max_context_tokens),
        ):
            if value is not None and value < 1:
                raise ValueError(f"{name} must be at least 1")
        if self.candidate_top_k > 500:
            raise ValueError("candidate_top_k must not exceed 500")
        if self.min_relevance_score is not None and self.min_relevance_score < 0:
            raise ValueError("min_relevance_score must be non-negative")
        if not 0.0 < self.overlap_threshold <= 1.0:
            raise ValueError("overlap_threshold must be in (0, 1]")
