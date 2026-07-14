"""Shared data contracts used by every CodeRAG module."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Repository(ContractModel):
    id: str
    name: str
    source: str | None = None
    revision: str
    root_path: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class FileMetadata(ContractModel):
    id: str
    repository_id: str
    revision: str
    path: str
    extension: str
    language: str
    size_bytes: int = Field(ge=0)
    line_count: int = Field(ge=0)
    content_hash: str
    is_test: bool = False
    is_config: bool = False
    is_docs: bool = False


class RepositoryFile(ContractModel):
    metadata: FileMetadata
    raw_content: str


class Issue(ContractModel):
    id: str
    repository_id: str
    title: str
    body: str = ""
    labels: list[str] = Field(default_factory=list)
    expected_files: list[str] = Field(default_factory=list)


class ChunkingConfig(ContractModel):
    strategy: str = "ast_aware"
    fallback_strategy: str = "fixed_window"
    max_chunk_lines: int = Field(default=80, ge=1)
    overlap_lines: int = Field(default=10, ge=0)
    include_metadata: bool = True


class RetrievalConfig(ContractModel):
    top_k: int = Field(default=10, ge=1)
    use_bm25: bool = True
    use_dense: bool = True
    use_ast_candidates: bool = True
    fusion_method: str = "rrf"


class EmbeddingConfig(ContractModel):
    model: str = "jinaai/jina-embeddings-v2-base-code"
    normalize_vectors: bool = True
    batch_size: int = Field(default=32, ge=1)


class RerankerConfig(ContractModel):
    """Configuration for the cross-encoder reranking stage (after RRF).

    ``reranker_top_k`` is the size of the RRF candidate pool fed to the reranker;
    ``final_top_k`` is how many reranked evidence chunks are returned. Both are
    tuned in the Sprint 2 experiment matrix.
    """

    enabled: bool = True
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    device: str = "cpu"
    batch_size: int = Field(default=32, ge=1)
    reranker_top_k: int = Field(default=50, ge=1)
    final_top_k: int = Field(default=10, ge=1)
    max_pair_chars: int = Field(default=2000, ge=1)


class ExperimentConfig(ContractModel):
    """Configuration for one retrieval experiment run.

    This model describes which retrievers are active, how many candidates each
    stage keeps, and whether RRF/reranking are part of the run. It is intentionally
    storage-agnostic so the same config can drive in-memory and DB-backed runs.
    """

    name: str

    use_bm25: bool = True
    use_dense: bool = True
    use_ast: bool = True
    use_rrf: bool = True
    use_reranker: bool = True

    bm25_top_k: int = Field(default=50, ge=1)
    dense_top_k: int = Field(default=50, ge=1)
    ast_top_k: int = Field(default=50, ge=1)

    rrf_k: int = Field(default=60, ge=0)
    rrf_top_k: int = Field(default=50, ge=1)

    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    reranker_top_k: int = Field(default=50, ge=1)
    final_top_k: int = Field(default=10, ge=1)
    reranker_device: str = "cpu"
    reranker_batch_size: int = Field(default=32, ge=1)
    reranker_max_pair_chars: int = Field(default=2000, ge=1)

    embedding_model: str = "jinaai/jina-embeddings-v2-base-code"
    random_seed: int = 42

    @model_validator(mode="after")
    def validate_pipeline_shape(self) -> ExperimentConfig:
        enabled_retrievers = sum((self.use_bm25, self.use_dense, self.use_ast))
        if enabled_retrievers == 0:
            raise ValueError("at least one retriever must be enabled")
        if enabled_retrievers > 1 and not self.use_rrf:
            raise ValueError("multiple retrievers require RRF fusion")
        if self.use_reranker and not self.use_rrf:
            raise ValueError("reranker requires RRF candidates")
        if self.use_reranker and self.reranker_top_k > self.rrf_top_k:
            raise ValueError("reranker_top_k must be less than or equal to rrf_top_k")
        if self.use_reranker and self.final_top_k > self.reranker_top_k:
            raise ValueError("final_top_k must be less than or equal to reranker_top_k")
        if not self.use_reranker and self.final_top_k > self.rrf_top_k:
            raise ValueError("final_top_k must be less than or equal to rrf_top_k")
        return self


class TwoStageConfig(ContractModel):
    """Configuration for a two-stage run: rank files, then rank chunks inside them.

    ``stage2`` is an ordinary :class:`ExperimentConfig`; it just sees the chunks of the
    stage-1 candidates instead of the whole repository. The fields here are the knobs
    that only exist because retrieval happens in two passes.
    """

    name: str

    file_top_n: int = Field(default=100, ge=1)
    """Files kept by stage-1 BM25. This is a hard cut: a file outside it can never be
    retrieved, so ``file_top_n`` is the ceiling on the whole pipeline's recall."""

    expand_references: int = Field(default=0, ge=0)
    """Extra files pulled in because a stage-1 hit names their symbol (0 disables)."""

    exclude_tests: bool = True
    """Drop test files from the stage-1 index. They restate the bug they cover, so they
    outrank the source file that has to change, and they are never the expected answer."""

    max_chunks_per_file: int | None = Field(default=None, ge=1)
    """Cap on how many chunks one file may contribute to the final evidence. Without it a
    single file can take most of ``final_top_k`` with overlapping class/method chunks."""

    stage2: ExperimentConfig


class AIConfig(ContractModel):
    version: int = 1
    include: list[str] = Field(default_factory=lambda: ["**/*"])
    exclude: list[str] = Field(default_factory=list)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    reranker: RerankerConfig = Field(default_factory=RerankerConfig)


class CodeChunk(ContractModel):
    id: str
    parent_chunk_id: str | None = None
    split_index: int | None = Field(default=None, ge=1)
    split_count: int | None = Field(default=None, ge=1)
    repository_id: str
    file_id: str
    path: str
    language: str
    chunk_type: Literal["ast", "fixed_window", "file"]
    node_type: str | None = None
    symbol_name: str | None = None
    parent_symbol: str | None = None
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    content: str
    content_hash: str
    token_count: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_split_metadata(self) -> CodeChunk:
        split_fields = (self.parent_chunk_id, self.split_index, self.split_count)
        if not any(value is not None for value in split_fields):
            return self

        if self.parent_chunk_id is None or self.split_index is None or self.split_count is None:
            raise ValueError(
                "parent_chunk_id, split_index, and split_count must be set together"
            )
        if self.split_index > self.split_count:
            raise ValueError("split_index must be less than or equal to split_count")
        return self


class StructuralMetadata(ContractModel):
    chunk_id: str
    imports: list[str] = Field(default_factory=list)
    calls: list[str] = Field(default_factory=list)
    defined_symbols: list[str] = Field(default_factory=list)
    referenced_symbols: list[str] = Field(default_factory=list)
    flags: dict[str, bool] = Field(default_factory=dict)


class ChunkSearchTexts(ContractModel):
    chunk_id: str
    bm25_text: str
    embedding_text: str


class ChunkKeywords(ContractModel):
    chunk_id: str
    identifiers: list[str] = Field(default_factory=list)
    identifier_tokens: list[str] = Field(default_factory=list)
    string_literals: list[str] = Field(default_factory=list)
    comments_terms: list[str] = Field(default_factory=list)
    path_tokens: list[str] = Field(default_factory=list)


class ChunkEmbedding(ContractModel):
    chunk_id: str
    embedding_model: str
    vector: list[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChunksWithMetadata(ContractModel):
    chunks: list[CodeChunk]
    metadata: dict[str, StructuralMetadata]


class RepositoryBundle(ContractModel):
    """All persisted search artifacts needed to run retrieval for one repo revision."""

    repository_id: str
    revision: str
    chunks: list[CodeChunk]
    metadata: dict[str, StructuralMetadata]
    embeddings: list[ChunkEmbedding]
    keywords: dict[str, ChunkKeywords] = Field(default_factory=dict)
    search_texts: dict[str, ChunkSearchTexts] = Field(default_factory=dict)


class ExperimentRun(ContractModel):
    id: str
    name: str
    description: str = ""
    repository_id: str
    revision: str
    ai_config: dict[str, Any] = Field(default_factory=dict)
    embedding_model: str
    status: Literal["running", "completed", "failed"] = "running"
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None


class RetrievalRun(ContractModel):
    id: str
    repository_id: str
    issue_id: str
    query_text: str
    query_keywords: list[str] = Field(default_factory=list)
    top_k: int = Field(ge=1)
    retrieval_config: dict[str, Any] = Field(default_factory=dict)
    experiment_run_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RetrievalResult(ContractModel):
    chunk_id: str
    rank: int = Field(ge=1)
    score: float
    source: Literal["bm25", "dense", "ast", "rrf", "reranker"]
    bm25_score: float | None = None
    dense_score: float | None = None
    ast_score: float | None = None
    rrf_score: float | None = None
    reranker_score: float | None = None


class EvidenceScores(ContractModel):
    bm25: float | None = None
    dense: float | None = None
    ast: float | None = None
    rrf: float | None = None
    reranker: float | None = None


class EvidenceChunk(ContractModel):
    chunk_id: str
    repository_id: str
    path: str
    language: str
    node_type: str | None = None
    symbol_name: str | None = None
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    content: str
    scores: EvidenceScores = Field(default_factory=EvidenceScores)
    source_signals: list[Literal["bm25", "dense", "ast", "rrf", "reranker"]] = Field(
        default_factory=list
    )


class EvidenceBuildWarning(ContractModel):
    code: str
    message: str
    chunk_id: str | None = None


class EvidenceBuildResult(ContractModel):
    evidence_chunks: list[EvidenceChunk]
    warnings: list[EvidenceBuildWarning] = Field(default_factory=list)


class RetrievalPipelineResult(ContractModel):
    retrieval_run_id: str | None = None
    evidence: EvidenceBuildResult
    results: list[RetrievalResult] = Field(default_factory=list)
