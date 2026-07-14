# Data Contracts

`src/gitflame_coderag/schemas.py` is the executable source of truth. All modules must exchange
those models or values explicitly derived from them. Do not introduce competing dictionaries with
different field names.

## Ownership

| Area | Owner | Package |
|---|---|---|
| Schemas and AST chunking | Danil | `schemas.py`, `chunking/`, `retrieval/ast.py` |
| Repository ingestion | Kirill | `config/`, `ingestion/` |
| BM25 | Zhenya | `retrieval/bm25.py` |
| Reranking and final ranking | Zhenya | `retrieval/reranker.py` |
| Embeddings and dense search | Karim | `embeddings/`, `retrieval/dense.py` |
| Persistence | Martin | `storage/`, `migrations/` |

## Function Contracts

### Ingestion

```python
load_repository_files(repo_path: Path, repository_id: str, revision: str) -> list[RepositoryFile]
load_ai_config(config_path: Path) -> dict[str, Any]
parse_ai_config(raw_config: dict[str, Any]) -> AIConfig
filter_files_by_config(files: list[RepositoryFile], config: AIConfig) -> list[RepositoryFile]
detect_language(path: Path, content: str) -> str
build_file_metadata(path: Path, content: str, repository_id: str, revision: str) -> FileMetadata
```

### GitHub dataset collection

`ingestion/github.py` builds dataset entries from real GitHub repositories, driven by
`scripts/fetch_github_dataset.py` (`discover` -> manifest, `fetch` -> dataset). It writes
`datasets/original_repositories/<repository_id>/{code/, repo.yml}` and **never** writes
`issues.jsonl`, which is authored by hand.

```python
discover_repositories(client: GitHubClient, *, languages: list[str], filters: FileFilters, limit: int, ...) -> list[RepoCandidate]
fetch_repository(client: GitHubClient, spec: RepoSpec, dest_root: Path, filters: FileFilters | None = None, *, issues_source: str = "github", force: bool = False) -> FetchResult
select_files(entries: Iterable[TreeEntry], filters: FileFilters, *, subdir: str | None = None) -> list[TreeEntry]
build_repo_config(metadata: dict[str, Any], commit: str, paths: list[str], ...) -> dict[str, Any]
load_manifest(path: Path) -> list[RepoSpec]
```

`FileFilters` is the dataset budget: `max_files` (default 100), `min_files`, `max_file_bytes`,
the source-extension whitelist (`LANGUAGES_BY_EXTENSION`) and the exclude globs. The file count
is measured on the Git Trees API response, so an over-budget repository is rejected before it is
downloaded. Fetching pins a commit sha: it lands in `repo.yml` as `repository.revision` and is
the `revision` to pass to `load_repository_files`.

The `analysis.include` / `analysis.exclude` patterns written into a generated `repo.yml` select
exactly the files that were copied into `code/` — the generator and `filter_files_by_config`
share the glob implementation, so the round trip is exact.

### Chunking

```python
chunk_file_with_ast_grep(file: RepositoryFile, config: AIConfig) -> list[CodeChunk]
chunk_file_fallback_window(file: RepositoryFile, config: AIConfig) -> list[CodeChunk]
build_chunks(files: list[RepositoryFile], config: AIConfig) -> list[CodeChunk]
extract_structural_metadata(chunk: CodeChunk) -> StructuralMetadata
```

### Search representations

```python
build_bm25_text(chunk: CodeChunk, metadata: StructuralMetadata) -> str
build_embedding_text(chunk: CodeChunk, metadata: StructuralMetadata) -> str
extract_keywords_from_chunk(chunk: CodeChunk) -> ChunkKeywords
```

### Retrieval

```python
build_bm25_index(chunks: list[CodeChunk]) -> BM25Index
bm25_search(query: str, index: BM25Index, top_k: int) -> list[RetrievalResult]
dense_search(query_vector: list[float], embeddings: list[ChunkEmbedding], top_k: int) -> list[RetrievalResult]
dense_retrieval_pgvector(
    query: str,
    vector_store: Any,
    top_k: int,
    embedding_model: str,
    repository_id: str | None = None,
    revision: str | None = None,
) -> list[RetrievalResult]
ast_candidate_search(keywords: list[str], chunks: list[CodeChunk], top_k: int) -> list[RetrievalResult]
rrf_fusion(rankings: list[list[RetrievalResult]], top_k: int, rrf_k: int = 60) -> list[RetrievalResult]
build_evidence_scores(result: RetrievalResult) -> EvidenceScores
build_evidence_chunks(results: list[RetrievalResult], chunks_by_id: dict[str, CodeChunk], top_k: int | None = None) -> EvidenceBuildResult
```

`build_evidence_chunks()` returns `EvidenceBuildResult`: final `evidence_chunks` plus `warnings`.
Missing chunks are reported as `EvidenceBuildWarning(code="missing_chunk", chunk_id=...)` and the
builder continues, so experiments do not fail silently or stop on one inconsistent result.

### Metrics

```python
compute_recall_at_k(results: list[RetrievalResult], relevant_chunk_ids: set[str], k: int) -> float
compute_mrr(results: list[RetrievalResult], relevant_chunk_ids: set[str], k: int | None = None) -> float
compute_map_ndcg(runs: list[tuple[list[RetrievalResult], set[str]]], k: int) -> dict[str, float]
```

### Experiment Config (Sprint 2)

`ExperimentConfig` describes one retrieval experiment mode: enabled retrievers, per-stage top-k
limits, RRF parameters, reranker settings, embedding model, and random seed.

```python
ExperimentConfig(
    name: str,
    use_bm25: bool = True,
    use_dense: bool = True,
    use_ast: bool = True,
    use_rrf: bool = True,
    use_reranker: bool = True,
    bm25_top_k: int = 50,
    dense_top_k: int = 50,
    ast_top_k: int = 50,
    rrf_k: int = 60,
    rrf_top_k: int = 50,
    reranker_model: str = "BAAI/bge-reranker-v2-m3",
    reranker_top_k: int = 50,
    final_top_k: int = 10,
    reranker_device: str = "cpu",
    reranker_batch_size: int = 16,
    reranker_max_pair_chars: int = 8000,
    embedding_model: str = "jinaai/jina-embeddings-v2-base-code",
    random_seed: int = 42,
)
```

Validation rules: at least one retriever must be enabled; multiple retrievers require RRF;
reranker requires RRF candidates; `final_top_k <= reranker_top_k <= rrf_top_k` when reranker is on.

### Experiment Runner (Sprint 2)

```python
run_experiment_suite(
    repository: CodeRAGRepository,
    configs: list[ExperimentConfig],
    repositories: list[tuple[str, str]],  # repository_id, revision
    *,
    issue_ids_by_repository: dict[str, list[str]] | None = None,
    reranker_model: CrossEncoderLike | None = None,
) -> ExperimentSuiteResult
```

The runner creates `ExperimentRun` records, executes `run_retrieval_from_db()` for each selected
issue, persists retrieval runs/results through the DB wrapper, records per-issue latency, and keeps
per-issue failures isolated. It does not compute metrics; metrics are a separate layer.

### Reranking (Sprint 2)

The reranker is a stage **after** RRF: it rescores the fused candidates with a cross-encoder and
returns the final top-k ordering. It consumes the RRF `RetrievalResult` list plus a
`chunk_id -> CodeChunk` lookup (for the chunk content) and returns `RetrievalResult` objects with
`source="reranker"` and `reranker_score` populated; component scores (`bm25_score` / `dense_score` /
`ast_score` / `rrf_score`) are preserved. Reranked results map onto `EvidenceChunk.scores.reranker`
when building final evidence. When the model is unavailable the stage falls back to RRF order.

```python
load_reranker_model(model_name: str = ..., device: str = "cpu") -> CrossEncoderLike | None
build_reranker_input(query: str, chunk: CodeChunk, max_pair_chars: int = 8000) -> tuple[str, str]
score_query_chunk_pair(model: CrossEncoderLike, query: str, chunk: CodeChunk) -> float
rerank_candidates(query: str, candidates: list[RetrievalResult], chunks_by_id: dict[str, CodeChunk], model=None, *, top_k: int, ...) -> list[RetrievalResult]
reranker_fallback(candidates: list[RetrievalResult], *, top_k: int) -> list[RetrievalResult]
compare_rrf_vs_reranker(cases: list[RerankerCase], *, model=None, k_values=(1, 3, 5, 10), ...) -> dict
```

The default reranker model is `BAAI/bge-reranker-v2-m3`: its 8192-token window fits a whole AST
chunk, where the previous `cross-encoder/ms-marco-MiniLM-L-6-v2` had 512 and truncated 78% of the
chunks it scored. It is a plain sequence-classification XLM-R, so it needs no extra dependencies,
but it is 568M parameters — set `device: cpu` only for small pools. The model is configurable via
`AIConfig.reranker` (`RerankerConfig`). Tunable hyperparameters live there: `reranker_top_k` (RRF
candidate pool fed to the reranker) and `final_top_k` (final evidence count).

### Storage

Storage functions receive schema models and return persisted identifiers or schema models. Database
rows must not leak into retrieval and chunking packages.

```python
save_repository(repository: Repository) -> None
save_file_metadata(metadata: FileMetadata) -> None
save_issue(issue: Issue) -> None
save_chunk(chunk: CodeChunk) -> None
save_structural_metadata(metadata: StructuralMetadata) -> None
save_bm25_text(chunk_id: str, text: str) -> None
save_embedding_text(chunk_id: str, text: str) -> None
save_embedding_vector(embedding: ChunkEmbedding) -> None
save_chunk_embedding(embedding: ChunkEmbedding) -> None
load_chunk_embeddings(
    repository_id: str | None = None,
    revision: str | None = None,
    embedding_model: str | None = None,
) -> list[ChunkEmbedding]
create_vector_index(embedding_model: str, dimensions: int) -> str
search_similar_chunks(
    query_vector: list[float],
    embedding_model: str,
    top_k: int,
    repository_id: str | None = None,
    revision: str | None = None,
) -> list[RetrievalResult]
save_keywords(keywords: ChunkKeywords) -> None
save_retrieval_run(run: RetrievalRun) -> None
save_retrieval_results(retrieval_run_id: str, results: list[RetrievalResult]) -> None
save_experiment_run(experiment: ExperimentRun) -> None
load_issue(issue_id: str) -> Issue | None
load_chunks_for_repository(repository_id: str, revision: str) -> list[CodeChunk]
load_chunks_with_metadata(repository_id: str, revision: str) -> ChunksWithMetadata
load_chunk_embeddings(repository_id: str, revision: str, *, embedding_model: str | None = None) -> list[ChunkEmbedding]
load_repository_bundle(repository_id: str, revision: str, *, embedding_model: str | None = None) -> RepositoryBundle
```

## Invariants

- Raw source code and chunk content are never destructively normalized.
- Paths are repository-relative and use `/` separators.
- `start_line` and `end_line` are 1-based and inclusive.
- Every chunk belongs to exactly one file and repository revision.
- Split chunks use `parent_chunk_id` to point to the original large chunk id and
  `split_index` / `split_count` to preserve part order.
- Search texts and embeddings reference an existing `chunk_id`.
- Chunk embeddings are keyed by `(chunk_id, embedding_model)` so the main code embedding model
  can be compared with a lightweight baseline without overwriting vectors.
- Retrieval results always state their source and rank.
- Reranked results use `source="reranker"`, set `reranker_score`, and preserve upstream component
  scores; `reranker_score` stays `None` when the reranker did not run (fallback to RRF order).
- `RetrievalRun.experiment_run_id` is kept for Sprint 2 experiment tracking only. Before a
  production version, remove it from the normal retrieval path or move it behind a separate
  experiment-only adapter.
- `expected_chunks` is not required in Sprint 1.
