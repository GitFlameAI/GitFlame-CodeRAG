# GitFlame CodeRAG

GitFlame CodeRAG is a retrieval system for the GitFlame issue-to-plan and
issue-to-code workflows. Given a GitHub-like issue, it searches repository code
and returns top-k evidence chunks/files that can be passed to an LLM as grounded
context.

The project combines lexical, dense and structural code retrieval:

- **BM25** for keyword and code-symbol matching;
- **Jina code embeddings** for semantic retrieval;
- **AST-Grep / AST metadata** for structure-aware chunking and symbol signals;
- **RRF** for rank fusion;
- optional **cross-encoder reranking** for final candidate reordering.

## Repository Map

| Path | What is inside |
|---|---|
| `src/gitflame_coderag/` | Main Python package. |
| `src/gitflame_coderag/config/` | Loading and parsing `repo.yml` configs. |
| `src/gitflame_coderag/ingestion/` | Repository files, issues, GitHub dataset loading and file filtering. |
| `src/gitflame_coderag/chunking/` | AST-Grep chunking, fallback window chunking and structural metadata extraction. |
| `src/gitflame_coderag/retrieval/` | BM25, dense retrieval, AST retrieval, RRF, reranker, evidence formatting and metrics. |
| `src/gitflame_coderag/embeddings/` | Embedding service and persistent embedding cache helpers. |
| `src/gitflame_coderag/storage/` | PostgreSQL / pgvector storage layer and experiment result tables. |
| `src/gitflame_coderag/pipelines/` | Indexing, issue retrieval and two-stage retrieval orchestration. |
| `src/gitflame_coderag/experiments/` | Experiment runner helpers, file-level metrics and validation utilities. |
| `configs/` | Example repository and dataset collection configs. |
| `datasets/` | Prepared benchmark repositories, issues and dataset overview. See `datasets/README.md`. |
| `experiments/` | Final experiment summary, metrics and statistical interpretation. |
| `migrations/` | SQL migrations for PostgreSQL and pgvector tables. |
| `scripts/` | Dataset collection, embedding cache and experiment runner scripts. |
| `tests/` | Unit and integration tests. |
| `data_contracts.md` | Shared contracts for functions, stored entities and invariants. |
| `experiment_manifest.yml` | High-level manifest for experiment artifacts. |

## Local Setup

The project uses Python 3.12 and `uv`.

```bash
git clone https://github.com/kite121/GitFlame-CodeRAG.git
cd GitFlame-CodeRAG
uv sync --dev
cp .env.example .env
```

The default `.env.example` points to a local PostgreSQL database:

```text
postgresql+psycopg://gitflame:gitflame@localhost:5432/gitflame_coderag
```

## Run Tests

Unit tests do not require PostgreSQL:

```bash
uv run pytest tests/unit
```

Integration tests require PostgreSQL with pgvector. Start it with Docker:

```bash
docker compose up -d database
uv run pytest tests/integration
```

Run the full test suite:

```bash
docker compose up -d database
uv run pytest
```

Optional lint check:

```bash
uv run ruff check .
```

## Run Experiments

Experiment scripts write JSON outputs and include dataset summaries, model smoke
tests, metrics, latency and errors if something failed.

Run the original in-memory hybrid retrieval matrix:

```bash
uv run python scripts/run_original_models_experiment.py \
  --dataset-root datasets \
  --output results/original_models_experiment_results.json \
  --configs bm25_only,dense_only,ast_only,bm25_ast,bm25_dense,ast_dense,full_rrf,full_rrf_reranker \
  --k-values 5,10,15
```

Run the optimized two-stage retrieval matrix:

```bash
uv run python scripts/run_two_stage_experiment.py \
  --dataset-root datasets \
  --output results/two_stage.json \
  --configs bm25_only,dense_only,bm25_dense,bm25_dense_capped,bm25_dense_reranker,bm25_dense_reranker_capped \
  --k-values 5,10,15
```

For large repositories, prebuilding the embedding cache can make repeated runs
much faster:

```bash
uv run python scripts/build_embedding_cache.py --dataset-root datasets
```

Full experiment runs use HuggingFace models and can require significant RAM/VRAM.
The default models are:

| Model | Role |
|---|---|
| `jinaai/jina-embeddings-v2-base-code` | Code embedding model |
| `BAAI/bge-reranker-v2-m3` | Cross-encoder reranker |

## Results

The final experiment summary is in `experiments/README.md`.

Main conclusions:

- on the original multi-repository benchmark, `bm25_dense` was the best practical
  quality-oriented approach;
- on the large Elasticsearch benchmark, the optimized `bm25_dense_capped`
  two-stage approach had the best `MAP@10` and `Recall@10`;
- the `MAP@10` improvement of `bm25_dense_capped` over `bm25_only` was
  statistically confirmed on the Elasticsearch benchmark after Bonferroni
  correction;
- reranker variants increased latency and did not improve `MAP@10` in the final
  experiments.

## Data Format

Each dataset repository follows this layout:

```text
datasets/repositories/<repo_id>/
  repo.yml
  issues.jsonl
  code/
```

- `repo.yml` controls included/excluded files, language detection and chunking
  settings.
- `issues.jsonl` contains GitHub-like issues and expected relevant files.
- `code/` contains the repository source files used for retrieval.

See `datasets/README.md` and `data_contracts.md` for details.
