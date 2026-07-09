# Sprint 3: Vector Storage, Indexing, Deployment and Maintenance

This note covers Karim's Sprint 3 handoff for the final presentation sections:
`Vector storage / indexing` and `Deployment / maintenance`.

## Presentation Summary

GitFlame CodeRAG stores repository chunks, search texts, structural metadata,
keywords and embeddings in PostgreSQL with pgvector. Raw source code stays in the
database as the source of truth, while BM25 text, embedding text and vector
representations are stored as derived artifacts. Dense retrieval uses a pgvector
HNSW or IVFFlat index per embedding model and vector dimension, then filters by
repository and revision.

Deployment is intentionally simple: one Python 3.12 application process for
indexing and retrieval, one PostgreSQL 16 database with pgvector, and optional GPU
workers only for faster embedding rebuilds or reranking. The online query path can
run on CPU for the current course-scale dataset, while batch embedding generation
benefits most from GPU acceleration.

## Vector Storage and Indexing

### Stored Entities

The storage schema is centered on `code_chunks.id`. Each chunk has:

| Table | Purpose |
|---|---|
| `repositories` | Repository id, name, source, revision and root path. |
| `repository_files` | Repository-relative path, language, size, content hash and raw file content. |
| `code_chunks` | Raw chunk content, path, line range, AST node type, symbol names and content hash. |
| `chunk_structural_metadata` | Imports, calls, defined symbols, referenced symbols and structural flags. |
| `chunk_search_texts` | Derived `bm25_text` and `embedding_text`; raw code is not overwritten. |
| `chunk_keywords` | Identifiers, split identifier tokens, string literals, comments terms and path tokens. |
| `chunk_embeddings` | pgvector embedding, embedding model name and creation timestamp. |
| `retrieval_runs`, `retrieval_results` | Query audit trail, ranks and component scores. |

### Embedding Model Isolation

Embeddings are keyed by:

```sql
PRIMARY KEY (chunk_id, embedding_model)
```

This lets the project store multiple vector spaces side by side, for example:

- `jinaai/jina-embeddings-v2-base-code` as the primary code embedding model;
- `sentence-transformers/all-MiniLM-L6-v2` as a lightweight baseline.

The same chunk can therefore have a 768-dimensional Jina vector and a
384-dimensional MiniLM vector without overwriting either representation.

### pgvector Index

The storage adapter creates model-specific vector indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_chunk_embeddings_<model>_<dim>_<method>_<distance>
ON chunk_embeddings
USING hnsw ((embedding::vector(<dimensions>)) vector_cosine_ops)
WITH (m = 16, ef_construction = 64)
WHERE embedding_model = '<embedding_model>';
```

Default recommendation:

- use cosine distance because embeddings are normalized;
- use HNSW for interactive retrieval because it gives good recall/latency trade-offs;
- keep IVFFlat as a cheaper alternative for rebuild-heavy experiments;
- build one partial index per embedding model and dimension;
- keep `idx_chunk_embeddings_model` for filtering and model-specific maintenance.

Dense retrieval flow:

1. Embed issue title/body into a query vector with the selected `embedding_model`.
2. Search `chunk_embeddings` with pgvector cosine distance.
3. Join `code_chunks` and `repository_files` to filter by `repository_id` and `revision`.
4. Return `RetrievalResult(source="dense")` with rank and dense score.
5. Feed dense candidates into RRF together with BM25 and AST candidates.

## Updating Vectors

### Adding a New Repository

Recommended indexing sequence:

1. Load repository files and parse `repo.yml`.
2. Filter files by config.
3. Build AST-aware chunks with fallback chunking.
4. Save files, chunks, structural metadata, BM25 text, embedding text and keywords.
5. Batch-generate embeddings for all new chunks.
6. Upsert rows into `chunk_embeddings`.
7. Create or refresh the pgvector index for each embedding model.

### Incremental Updates

Use `content_hash` on files and chunks as the invalidation signal:

- unchanged chunk hash: keep existing `chunk_embeddings` row;
- changed chunk hash: rebuild `embedding_text`, regenerate the vector and upsert it;
- deleted chunk: remove the stale chunk row, relying on foreign-key cascade for search texts,
  metadata, keywords and embeddings;
- new embedding model: generate a second vector row for every selected chunk under the new
  `embedding_model`;
- model upgrade: keep the old model during comparison, then delete or archive it after metrics
  confirm the replacement.

For 500k chunks, vector regeneration should run as a batch job, not inside the online query path.
The query service should keep serving the previous model/index until the new vectors and index are
ready.

## Deployment Requirements

### Runtime Dependencies

Required:

- Python 3.12;
- `uv` for dependency management;
- PostgreSQL 16 with pgvector;
- project Python packages from `pyproject.toml`: `sqlalchemy`, `psycopg[binary]`,
  `pgvector`, `pydantic`, `pyyaml`, `rank-bm25`, `numpy`, `sentence-transformers`
  and `transformers`;
- persistent PostgreSQL volume for indexed repositories and embeddings.

Optional but useful:

- NVIDIA GPU with CUDA for faster embedding generation and reranking;
- separate worker process for indexing and embedding rebuilds;
- scheduled backup for the PostgreSQL volume.

### Hardware Profiles

| Profile | CPU | GPU | RAM | Disk | Use case |
|---|---:|---:|---:|---:|---|
| Local demo | 4 cores | Not required | 8-16 GB | 20 GB | Current course demo and small repositories. |
| 500k-chunk CPU deployment | 8-16 cores | Not required | 32 GB | 50-100 GB SSD | Interactive retrieval with precomputed embeddings. |
| 500k-chunk indexing worker | 8-16 cores | 12-24 GB VRAM recommended | 32-64 GB | 100 GB SSD | Batch embedding generation and reranker experiments. |
| Production-like setup | 16+ cores | Optional | 64 GB | 100+ GB SSD, backups enabled | Concurrent users, rebuild jobs and retained experiment runs. |

Disk estimate for 500k chunks:

- 768-dimensional float32 vectors: about 1.43 GiB per embedding model before database and index
  overhead;
- 384-dimensional float32 vectors: about 0.72 GiB per embedding model before overhead;
- HNSW index, table metadata, raw chunk content, search texts and experiment results can multiply
  this several times, so 50-100 GB SSD is a practical planning range.

### Latency Estimates

These are planning estimates and depend on hardware, chunk count, index settings and candidate
depth.

| Stage | Expected latency |
|---|---:|
| Query embedding | 50-300 ms on GPU, 200-1500 ms on CPU. |
| pgvector HNSW dense search over 500k vectors | 50-200 ms when warm and indexed. |
| BM25 candidate retrieval | 50-500 ms depending on in-memory index size. |
| AST candidate retrieval | 50-500 ms depending on keyword filters and chunk metadata. |
| RRF fusion | Below 50 ms for candidate pools up to a few hundred chunks. |
| Cross-encoder reranker over top 50 | 100-500 ms on GPU, 1-5 s on CPU. |

For the best latency/quality trade-off, use `Full RRF` for fast responses and
`Full RRF + Reranker` when quality matters more than latency.

### Cost Model

The default setup uses local open-source models, so there is no per-query API cost. Costs are
infrastructure costs:

- CPU-only demo: laptop or small VM cost only;
- 500k-chunk interactive service: one mid-size CPU VM plus managed PostgreSQL or a Postgres VM;
- embedding rebuilds: the main variable cost, best handled by short-lived GPU workers;
- storage: SSD capacity for raw code, embeddings, indexes, retrieval logs and backups.

To reduce cost:

- precompute all chunk embeddings;
- cache loaded embedding and reranker models in process;
- rebuild only chunks whose `content_hash` changed;
- keep only necessary experiment runs and old embedding models;
- run reranker only after RRF has reduced the candidate pool.

## Short Deployment Plan

1. Start PostgreSQL with pgvector, for example through `docker compose up -d database`.
2. Configure `DATABASE_URL`.
3. Run migrations from `migrations/`.
4. Run repository indexing as an offline or scheduled job.
5. Build pgvector indexes for the selected embedding model and dimension.
6. Start the retrieval API/demo process.
7. Monitor query latency, database size, failed indexing jobs and stale embeddings.

