# Retrieval Experiments

This folder documents the experiments that were actually run for GitFlame CodeRAG.
The main target is issue-to-evidence retrieval: given an issue, return relevant
code chunks/files with measurable quality and latency.

## What Was Tested

| Benchmark | Scope | Main result files | Tested approaches |
|---|---:|---|---|
| Original hybrid retrieval | 114 repos, 560 issues, 37,833 chunks | `stage1_original.json`, `stage3_original.json` | `bm25_only`, `dense_only`, `ast_only`, `bm25_ast`, `bm25_dense`, `ast_dense`, `full_rrf`, `full_rrf_reranker` |
| Two-stage Elasticsearch retrieval | 1 large repo, 75 issues, 450 approach-issue rows | `two_stage_elasticsearch4.json`, `two_stage_elasticsearch5.json` | `bm25_only`, `dense_only`, `bm25_dense`, `bm25_dense_capped`, `bm25_dense_reranker`, `bm25_dense_reranker_capped` |

## Models And Components

| Component | Used value | Role |
|---|---|---|
| Dense embedding model | `jinaai/jina-embeddings-v2-base-code` | Code-oriented dense vectors for chunks and queries |
| Lightweight embedding baseline | `sentence-transformers/all-MiniLM-L6-v2` | Fast sanity-check baseline for local runs |
| Vector distance | Cosine similarity | Dense retrieval scoring |
| Lexical retriever | BM25 | Strong keyword/code-symbol baseline |
| Structural retriever | AST metadata / AST-Grep chunks | Uses symbols, calls, imports and structural metadata |
| Fusion | RRF | Combines BM25, dense and AST ranks |
| Reranker | Cross-encoder reranker variants | Tested as final reordering step |

## Metrics

| Metric | Why it matters |
|---|---|
| `Recall@K` | Measures whether relevant evidence appears in top-k. |
| `Precision@K` | Measures how much irrelevant evidence is mixed into top-k. |
| `MAP@K` | Primary quality metric: rewards relevant evidence appearing higher in the ranking. |
| `Avg latency` / `P95 latency` | Shows practical runtime cost per issue. |

Final reporting uses `K = 5, 10, 15`, with `MAP@10` as the primary statistical
comparison metric.

## Original Hybrid Retrieval Results

Best quality-oriented approach: `bm25_dense`.

| Approach | Recall@10 | Precision@10 | MAP@10 | Avg latency, s |
|---|---:|---:|---:|---:|
| `bm25_only` | 0.932 | 0.402 | 0.781 | 0.0031 |
| `dense_only` | 0.938 | 0.401 | 0.769 | 0.0125 |
| `ast_only` | 0.871 | 0.324 | 0.648 | 0.0005 |
| `bm25_dense` | **0.949** | **0.416** | **0.794** | 0.0150 |
| `full_rrf` | 0.935 | 0.401 | 0.777 | 0.0155 |
| `full_rrf_reranker` | 0.941 | 0.414 | 0.770 | 0.1429 |

Interpretation: for the original multi-repository benchmark, `bm25_dense` is the
best practical option. The reranker was slower and did not improve `MAP@10`.

## Two-Stage Elasticsearch Results

Best quality-oriented approach for this benchmark: `bm25_dense_capped`.

`bm25_dense_capped` was added as an optimized second iteration for large
repositories. It limits the candidate set before final ranking, reducing noise
and making the retrieval pipeline more practical on a large codebase.

| Approach | Recall@10 | Precision@10 | MAP@10 | Avg latency, s | P95 latency, s |
|---|---:|---:|---:|---:|---:|
| `bm25_only` | 0.653 | 0.609 | 0.457 | 6.0836 | 9.7380 |
| `dense_only` | 0.612 | 0.629 | 0.454 | **0.0701** | **0.1163** |
| `bm25_dense` | 0.642 | **0.691** | 0.479 | 3.2662 | 5.1892 |
| `bm25_dense_capped` | **0.782** | 0.452 | **0.532** | 3.2870 | 5.4211 |
| `bm25_dense_reranker` | 0.637 | 0.475 | 0.377 | 10.9875 | 14.5796 |
| `bm25_dense_reranker_capped` | 0.717 | 0.365 | 0.405 | 10.8992 | 14.5634 |

Interpretation: `bm25_dense_capped` gives the best `Recall@10` and `MAP@10`.
`bm25_dense` gives the best `Precision@10`, while `dense_only` is the fastest.
Reranker variants are slower and worse on this benchmark.

## Statistical Significance

Baseline: `bm25_only`. Primary metric: `MAP@10`. Bonferroni correction was applied
over 5 candidate methods, so the corrected threshold is `alpha = 0.010`.

| Candidate | Delta MAP@10 | Wilcoxon p | Bonferroni p | Bootstrap 95% CI | Result |
|---|---:|---:|---:|---|---|
| `dense_only` | -0.003 | 0.806 | 1.000 | [-0.048, 0.044] | Not significant |
| `bm25_dense` | +0.022 | 0.608 | 1.000 | [-0.015, 0.062] | Not significant |
| `bm25_dense_capped` | **+0.075** | **<0.001** | **0.004** | **[0.035, 0.115]** | **Significant improvement** |
| `bm25_dense_reranker` | -0.080 | 0.003 | 0.013 | [-0.133, -0.028] | Negative raw effect; not accepted after correction |
| `bm25_dense_reranker_capped` | -0.052 | 0.081 | 0.405 | [-0.106, 0.002] | Not significant |

## Final Takeaway

| Scenario | Recommended approach | Reason |
|---|---|---|
| Small/mixed repository benchmark | `bm25_dense` | Best observed `MAP@10` and `Recall@10` with low latency. |
| Large Elasticsearch benchmark | `bm25_dense_capped` | Best `MAP@10` and `Recall@10`; `MAP@10` improvement over BM25 is statistically confirmed on this benchmark. |
| Lowest latency mode | `dense_only` or `ast_only` depending on dataset | Fastest options, but lower quality. |
| Reranker usage | Do not use by default | Current reranker configs increased latency and reduced `MAP@10`. |

Main limitation: the large-scale statistical confirmation is based on one large
repository, and relevance labels are file-level rather than exact chunk-level.
