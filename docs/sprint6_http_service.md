# Sprint 6: CodeRAG HTTP service

CodeRAG exposes the contract already consumed by CodePilot Agent Engine:

- `GET /health` checks database availability and does not require authentication;
- `POST /search` accepts `query`, `top_k` and repository filters;
- results contain only `path`, `start_line`, `end_line`, `score`, and `content`;
- an unknown repository/revision returns `{"results": []}` rather than invented evidence;
- `RAG_API_KEY`, when set, protects `/search` with a Bearer token.

The search pipeline uses BM25 plus dense retrieval/RRF when stored embeddings are available.
If dense query embedding fails, it falls back to BM25. Before returning context it applies the
configured minimum raw retrieval score, maximum chunks (`top_k`), maximum files, maximum chunks
per file, token budget, and overlapping-range deduplication. The response score is relative to
the best result in the current query and normalized to `[0, 1]`; it is not a probability.

## Local run

Copy `.env.example` to `.env`, set a new private `RAG_API_KEY`, then run:

```bash
docker compose up --build database rag-service
```

The repository revision must already be ingested and indexed in the CodeRAG database. The service
does not clone or index repositories during a search request.

Check readiness:

```bash
curl --fail http://localhost:8004/health
```

Run a contract smoke test (replace the repository and revision with indexed values):

```bash
curl --fail http://localhost:8004/search \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $RAG_API_KEY" \
  -d '{
    "query": "where is authentication validated?",
    "top_k": 5,
    "filters": {
      "repository_id": "owner/repository",
      "commit_sha": "indexed-commit-sha",
      "include": ["**/*"],
      "exclude": ["node_modules/**", ".git/**"]
    }
  }'
```

Expected checks: HTTP 200, no more than five results, every score is from 0 to 1, paths satisfy
include/exclude rules, line ranges are ordered, and content comes from the requested revision.

## CodePilot connection

Set these variables for the `agent-engine` service and restart it:

```dotenv
RAG_BASE_URL=http://rag-service:8004
RAG_API_KEY=<the same private key as CodeRAG>
MODEL_CONTEXT_LIMIT=32768
```

If CodeRAG is deployed outside the CodePilot Compose network, use its reachable HTTPS URL instead.
`32768` matches the context advertised by the current `laguna` endpoint. No Agent Engine code
change is required: `HttpRagClient` already calls these two endpoints.

## Quality check

For 10–20 known issues, record expected files and inspect top 5 results. At minimum report
Recall@5 (share of issues with an expected file in the top five), Precision@5, empty-result rate,
p50/p95 latency, and the number of results/files/tokens admitted by the context policy. Tune
`RAG_MIN_RELEVANCE_SCORE` only on this validation set because raw BM25/RRF scores are not calibrated
probabilities. Keep `top_k` and the hard budgets enabled even after threshold tuning.
