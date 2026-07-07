# Retrieval Experiments

Sprint 2 experiments compare lexical, dense, structural and hybrid retrieval modes for the
GitFlame CodeRAG issue-to-evidence pipeline. The detailed comparison matrix and statistical test
plan live in [`experiment_plan.md`](experiment_plan.md).

## Comparisons

| Experiment | Pipeline |
|---|---|
| `bm25_only` | BM25 |
| `dense_only` | Dense |
| `ast_only` | AST |
| `bm25_dense_rrf` | BM25 + Dense -> RRF |
| `bm25_ast_rrf` | BM25 + AST -> RRF |
| `dense_ast_rrf` | Dense + AST -> RRF |
| `full_rrf` | BM25 + Dense + AST -> RRF |
| `full_rrf_reranker` | BM25 + Dense + AST -> RRF -> Reranker |

## Metrics

| Metric | Purpose |
|---|---|
| `Recall@K` | Main retrieval metric: checks whether relevant files/chunks appear in top-k. |
| `Precision@K` | Measures how much irrelevant context is mixed into top-k. |
| `MAP@K` | Measures ranked-list quality across all relevant results in top-k. |
| `Latency per issue` | Tracks practical runtime cost per query. |

## Candidate Parameters

| Parameter | Candidate values |
|---|---|
| `final_top_k` | `5`, `10`, possibly `15` |
| `bm25_top_k` | `20`, `50`, `100` |
| `dense_top_k` | `20`, `50`, `100` |
| `ast_top_k` | `20`, `50`, `100` |
| `rrf_k` | `10`, `30`, `60` |
| `rrf_top_k` | `20`, `50`, `100` |
| `reranker_top_k` | `20`, `50` |
| `embedding_model` | lightweight baseline vs code-specific model |

Dense retrieval can compare the primary code model (`jinaai/jina-embeddings-v2-base-code`) against
a lightweight baseline (`sentence-transformers/all-MiniLM-L6-v2`). The pgvector storage layer keeps
embeddings under `(chunk_id, embedding_model)`, so multiple models can be indexed without
overwriting vectors.
