# GitFlame CodeRAG

Hybrid repository retrieval for GitFlame issue-to-plan and issue-to-code workflows.

The project indexes repository code as AST-aware chunks and retrieves evidence with BM25,
code embeddings, AST-Grep structural candidates, and Reciprocal Rank Fusion.

## Documentation

- `context.md`: complete project and Sprint context for humans and coding agents;
- `data_contracts.md`: shared function and storage contracts;
- `reports/sprint3_karim_deployment_vector_storage.md`: Sprint 3 handoff for vector storage,
  indexing, deployment and maintenance presentation sections;
- `schemas.py`: executable Pydantic schemas;
- `configs/repository.example.yml`: repository configuration template.

## Project Layout

```text
src/gitflame_coderag/
  config/       .yml loading and validation
  ingestion/    repository loading, filtering, file metadata
  chunking/     AST-Grep and fallback chunking
  retrieval/    BM25, dense, AST candidates, RRF
  embeddings/   embedding model adapter
  storage/      PostgreSQL/pgvector persistence
  pipelines/    indexing and issue retrieval orchestration
```

## Local Setup

```bash
uv sync --dev
docker compose up -d database
uv run pytest
```

## Sprint 1

Sprint 1 delivers datasets/config loading, shared contracts, AST-aware chunks, storage,
BM25 retrieval, and dense retrieval prototypes. See `context.md` for ownership and scope.
