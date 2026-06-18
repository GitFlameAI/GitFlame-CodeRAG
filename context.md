# Project Context: GitFlame Issue-to-Context RAG

## Purpose

This project is the Deep Learning / Search part connected to the main Capstone project `Capstone_GitFlame`.

The main Capstone project is about GitFlame CodePilot: an AI assistant for repository workflows. For this course project, we focus only on the retrieval/RAG part for the `issue-to-plan` and later `plan-to-code` scenario.

The goal is to build a retrieval pipeline that receives:

- repository code files;
- a GitHub/GitFlame-like issue;
- repository `.yml` configuration;

and returns:

- top-k evidence chunks from the repository;
- with file paths, line ranges, metadata, scores, and explanation;
- suitable for downstream plan/code generation.

Recommendations are out of scope for now. The current focus is `issue -> relevant code evidence`.

## High-Level Pipeline

```text
Repository files + .yml + Issue
        |
        v
Load repository files
        |
        v
Parse .yml and filter files
        |
        v
Build file metadata
        |
        v
AST-Grep chunking + fallback chunking
        |
        v
Store chunks, metadata, search texts, keywords, embeddings
        |
        v
Build issue query + extract issue keywords
        |
        v
BM25 retrieval + dense retrieval + AST candidate retrieval
        |
        v
RRF fusion
        |
        v
Top-k evidence chunks
```

## Key Design Decisions

### Raw Code Is Not Normalized

Original source code must be preserved as the source of truth.

Keep raw code unchanged because:

- line numbers must match the original repository;
- LLM evidence must show real code;
- AST-Grep and parsers depend on real syntax;
- downstream plan/code generation needs original formatting and context.

Normalization is used only for separate search representations:

- `bm25_text`;
- `embedding_text`;
- keywords;
- metadata tokens.

### Multiple Representations Per Code Chunk

Each code chunk should have several representations:

- raw chunk content;
- structural metadata from AST-Grep;
- BM25 text;
- embedding text;
- keywords;
- embedding vector;
- retrieval scores at query time.

This allows different rankers to use different signals while preserving the original code.

### AST-Grep Does Not Replace RAG

AST-Grep is a structural retrieval component, not a natural language retriever.

It is useful for:

- extracting functions/classes/methods;
- finding handlers, tests, configs;
- searching by symbols and structural patterns;
- generating structural candidates.

It does not directly answer natural language issues like:

```text
Recommendations disappear after refresh
```

Instead, the issue is converted into keywords/symbols/intent, and AST-Grep uses those signals to find structural candidates.

Final retrieval should combine:

```text
BM25 + dense embeddings + AST-Grep candidates -> RRF -> top-k evidence chunks
```

## Sprint 1 Scope

Sprint 1 is focused on:

- data collection;
- `.yml` config loading;
- file filtering;
- file metadata;
- AST-Grep chunking;
- fallback chunking;
- BM25 baseline;
- dense embeddings prototype;
- storage layer;
- shared schemas and contracts.

RRF, full experiments, final metrics, and full top-k integration may continue into Sprint 2, but Sprint 1 should prepare all pieces so they can be connected.

## Team Responsibilities For Sprint 1

### Danil

Role: architecture, schemas, data contracts, AST-Grep chunking.

Responsibilities:

- create `schemas.py`;
- create `data_contracts.md`;
- create and maintain this `context.md`;
- describe all entities, fields, function inputs, and outputs;
- define the shared chunk/result formats;
- implement AST-Grep chunking;
- implement fallback chunking;
- implement AST candidate retrieval.

Functions/artifacts:

- `schemas.py`
- `data_contracts.md`
- `context.md`
- `chunk_file_with_ast_grep()`
- `chunk_file_fallback_window()`
- `build_chunks()`
- `extract_structural_metadata()`
- `ast_candidate_search()`
- `rank_ast_candidates()`

### Kirill

Role: data collection and repository preparation.

Responsibilities:

- find 10-15 repositories;
- create one folder per repository;
- inside each repository folder, store code files;
- create 7 GitHub-like issues per repository;
- create `.yml` for each repository using the template from the repo;
- do not create `expected_chunks` in Sprint 1;
- include `expected_files` where possible;
- implement file loading and config filtering.

Functions:

- `load_repository_files()`
- `load_ai_config()`
- `parse_ai_config()`
- `filter_files_by_config()`
- `detect_language()`
- `build_file_metadata()`

Data produced:

- repository folders;
- code files;
- issues;
- `.yml` configs;
- file metadata.

### Zhenya

Role: BM25 retrieval.

Responsibilities:

- create BM25 text representation for chunks;
- implement tokenization and normalization for BM25;
- build BM25 index over chunks;
- implement BM25 top-k retrieval;
- return rank and score for each result.

Functions:

- `build_bm25_text()`
- `tokenize_for_bm25()`
- `build_bm25_index()`
- `build_bm25_query()`
- `bm25_search()`
- `rank_bm25_results()`

BM25 text should use:

- path tokens;
- language;
- symbol name;
- node type;
- imports/calls where available;
- normalized content tokens;
- split `snake_case`;
- split `camelCase`;
- original identifiers when useful.

### Karim

Role: embeddings and dense retrieval.

Responsibilities:

- choose a code embedding model;
- implement embedding text construction;
- extract keywords from chunks;
- embed chunks;
- embed issue queries;
- implement cosine similarity;
- implement dense top-k retrieval.

Functions:

- `build_embedding_text()`
- `extract_keywords_from_chunk()`
- `embed_text()`
- `embed_chunks()`
- `embed_query()`
- `cosine_similarity()`
- `dense_search()`
- `rank_dense_results()`

Embedding text should preserve code mostly as-is, but add useful context:

```text
File: backend/internal/app/server.go
Language: go
Symbol: handleAnalyzeIssue
Node type: function_declaration

Code:
...
```

### Martin

Role: storage layer.

Responsibilities:

- create database schema or migrations;
- save and load repositories;
- save and load file metadata;
- save chunks;
- save structural metadata;
- save BM25 text;
- save embedding text;
- save embedding vectors;
- save keywords;
- provide helper functions for loading chunks by repository.

Functions:

- `save_repository()`
- `save_file_metadata()`
- `save_chunk()`
- `save_structural_metadata()`
- `save_bm25_text()`
- `save_embedding_text()`
- `save_embedding_vector()`
- `save_keywords()`
- `load_chunks_for_repository()`

## Data Folder Structure

Recommended sample structure:

```text
sample_repositories/
  repo_001_fastapi_blog/
    repo.yml
    issues.jsonl
    code/
      ...
  repo_002_go_api/
    repo.yml
    issues.jsonl
    code/
      ...
```

Each `issues.jsonl` line should represent one issue:

```json
{
  "id": "repo_001_issue_001",
  "title": "Login returns 500 when token is expired",
  "body": "When an expired JWT is sent to /login/refresh, the server returns 500 instead of 401.",
  "labels": ["bug", "auth"],
  "expected_files": ["src/auth/routes.py", "src/auth/tokens.py"]
}
```

`expected_chunks` is not required in Sprint 1.

## Draft `.yml` Template

The actual template should live in the repository. All repository configs should follow it.

```yaml
version: 1

repository:
  name: sample-repository
  default_branch: main
  language_priority:
    - python
    - go
    - javascript
    - typescript

analysis:
  enabled: true
  include:
    - src/**
    - app/**
    - internal/**
    - backend/**
    - frontend/src/**
  exclude:
    - node_modules/**
    - dist/**
    - build/**
    - .git/**
    - vendor/**
    - __pycache__/**

issues:
  source: synthetic
  format: github_issue
  fields:
    - title
    - body
    - labels
    - expected_files

chunking:
  strategy: ast_aware
  fallback_strategy: fixed_window
  max_chunk_lines: 80
  overlap_lines: 10
  include_metadata: true

ast_grep:
  enabled: true
  extract_symbols: true
  extract_imports: true
  extract_handlers: true
  extract_tests: true

retrieval:
  top_k: 10
  use_bm25: true
  use_dense: true
  use_ast_candidates: true
  fusion_method: rrf

embeddings:
  model: server_controlled
  normalize_vectors: true
  batch_size: 32

storage:
  store_chunks: true
  store_embeddings: true
  store_retrieval_runs: true

evaluation:
  metrics:
    - precision_at_k
    - recall_at_k
    - mrr
    - ndcg_at_k
```

## Core Entities To Define In `schemas.py`

The exact implementation can use dataclasses or Pydantic models.

Required entities:

- `Repository`
- `RepositoryFile`
- `FileMetadata`
- `Issue`
- `AIConfig`
- `CodeChunk`
- `StructuralMetadata`
- `ChunkSearchTexts`
- `ChunkEmbedding`
- `ChunkKeywords`
- `RetrievalRun`
- `RetrievalResult`
- `EvidenceChunk`

## Important Fields

### Repository

- `id`
- `name`
- `source`
- `revision`
- `root_path`
- `created_at`

### RepositoryFile / FileMetadata

- `id`
- `repository_id`
- `revision`
- `path`
- `extension`
- `language`
- `size_bytes`
- `line_count`
- `content_hash`
- `raw_content`
- `is_test`
- `is_config`
- `is_docs`

### CodeChunk

- `id`
- `repository_id`
- `file_id`
- `path`
- `language`
- `chunk_type`
- `node_type`
- `symbol_name`
- `parent_symbol`
- `start_line`
- `end_line`
- `content`
- `content_hash`
- `token_count`

### StructuralMetadata

- `chunk_id`
- `imports`
- `calls`
- `defined_symbols`
- `referenced_symbols`
- `flags`

Example flags:

```json
{
  "is_handler": true,
  "is_test": false,
  "is_config": false,
  "has_error_handling": true
}
```

### ChunkSearchTexts

- `chunk_id`
- `bm25_text`
- `embedding_text`

### ChunkEmbedding

- `chunk_id`
- `embedding_model`
- `embedding`
- `created_at`

### ChunkKeywords

- `chunk_id`
- `identifiers`
- `identifier_tokens`
- `string_literals`
- `comments_terms`
- `path_tokens`

### Issue

- `id`
- `repository_id`
- `title`
- `body`
- `labels`
- `expected_files`

No `expected_chunks` in Sprint 1.

### RetrievalRun

- `id`
- `repository_id`
- `issue_id`
- `query_text`
- `query_keywords`
- `top_k`
- `retrieval_config`
- `created_at`

### RetrievalResult

- `id`
- `retrieval_run_id`
- `chunk_id`
- `rank`
- `bm25_score`
- `dense_score`
- `ast_score`
- `rrf_score`
- `evidence_reason`

### EvidenceChunk

This is the final output format for top-k retrieval.

```json
{
  "chunk_id": "repo:commit:path:start-end",
  "repository_id": "repo_1",
  "path": "backend/internal/app/server.go",
  "language": "go",
  "node_type": "function_declaration",
  "symbol_name": "handleAnalyzeIssue",
  "start_line": 42,
  "end_line": 91,
  "content": "...",
  "scores": {
    "bm25": 12.4,
    "dense": 0.82,
    "ast": 1.0,
    "rrf": 0.048
  },
  "evidence_reason": "Matched issue keywords and selected as HTTP handler by AST-Grep."
}
```

## Database Tables

Preferred architecture:

```text
PostgreSQL + pgvector
```

Prototype alternative:

```text
SQLite + local vector files / numpy arrays
```

Required tables:

- `repositories`
- `repository_files`
- `issues`
- `code_chunks`
- `chunk_structural_metadata`
- `chunk_search_texts`
- `chunk_embeddings`
- `chunk_keywords`
- `retrieval_runs`
- `retrieval_results`

## Table Sketch

### repositories

```sql
repositories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source TEXT,
    revision TEXT NOT NULL,
    root_path TEXT,
    created_at TIMESTAMP
)
```

### repository_files

```sql
repository_files (
    id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    revision TEXT NOT NULL,
    path TEXT NOT NULL,
    language TEXT,
    extension TEXT,
    size_bytes INTEGER,
    line_count INTEGER,
    content_hash TEXT,
    raw_content TEXT,
    is_test BOOLEAN,
    is_config BOOLEAN,
    is_docs BOOLEAN
)
```

### issues

```sql
issues (
    id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    labels JSON,
    expected_files JSON
)
```

### code_chunks

```sql
code_chunks (
    id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    file_id TEXT NOT NULL,
    path TEXT NOT NULL,
    language TEXT,
    chunk_type TEXT,
    node_type TEXT,
    symbol_name TEXT,
    parent_symbol TEXT,
    start_line INTEGER,
    end_line INTEGER,
    content TEXT,
    content_hash TEXT,
    token_count INTEGER
)
```

### chunk_structural_metadata

```sql
chunk_structural_metadata (
    chunk_id TEXT PRIMARY KEY,
    imports JSON,
    calls JSON,
    defined_symbols JSON,
    referenced_symbols JSON,
    flags JSON
)
```

### chunk_search_texts

```sql
chunk_search_texts (
    chunk_id TEXT PRIMARY KEY,
    bm25_text TEXT NOT NULL,
    embedding_text TEXT NOT NULL
)
```

### chunk_embeddings

For PostgreSQL + pgvector:

```sql
chunk_embeddings (
    chunk_id TEXT PRIMARY KEY,
    embedding_model TEXT NOT NULL,
    embedding VECTOR(768),
    created_at TIMESTAMP
)
```

The vector dimension depends on the selected embedding model.

### chunk_keywords

```sql
chunk_keywords (
    chunk_id TEXT PRIMARY KEY,
    identifiers JSON,
    identifier_tokens JSON,
    string_literals JSON,
    comments_terms JSON,
    path_tokens JSON
)
```

### retrieval_runs

```sql
retrieval_runs (
    id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    issue_id TEXT,
    query_text TEXT NOT NULL,
    query_keywords JSON,
    top_k INTEGER,
    retrieval_config JSON,
    created_at TIMESTAMP
)
```

### retrieval_results

```sql
retrieval_results (
    id TEXT PRIMARY KEY,
    retrieval_run_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    rank INTEGER,
    bm25_score REAL,
    dense_score REAL,
    ast_score REAL,
    rrf_score REAL,
    evidence_reason TEXT
)
```

## Function Groups

### Data Loading And Filtering

- `load_repository_files(repo_path, repository_id, revision) -> list[RepositoryFile]`
- `load_ai_config(config_path) -> dict`
- `parse_ai_config(raw_config) -> AIConfig`
- `filter_files_by_config(files, config) -> list[RepositoryFile]`
- `detect_language(path, content) -> str`
- `build_file_metadata(file) -> FileMetadata`

### Chunking

- `chunk_file_with_ast_grep(file, config) -> list[CodeChunk]`
- `chunk_file_fallback_window(file, config) -> list[CodeChunk]`
- `build_chunks(files, config) -> list[CodeChunk]`
- `extract_structural_metadata(chunk) -> StructuralMetadata`

### BM25

- `build_bm25_text(chunk, structural_metadata) -> str`
- `tokenize_for_bm25(text) -> list[str]`
- `build_bm25_index(chunks) -> BM25Index`
- `build_bm25_query(issue, config) -> str`
- `bm25_search(query, index, top_k) -> list[RetrievalResult]`
- `rank_bm25_results(results) -> list[RetrievalResult]`

### Embeddings

- `build_embedding_text(chunk, structural_metadata) -> str`
- `extract_keywords_from_chunk(chunk) -> ChunkKeywords`
- `embed_text(text) -> list[float]`
- `embed_chunks(chunks) -> list[ChunkEmbedding]`
- `embed_query(query) -> list[float]`
- `cosine_similarity(vector_a, vector_b) -> float`
- `dense_search(query_embedding, chunk_embeddings, top_k) -> list[RetrievalResult]`
- `rank_dense_results(results) -> list[RetrievalResult]`

### AST Candidate Retrieval

- `ast_candidate_search(issue_keywords, chunks, structural_metadata, top_k) -> list[RetrievalResult]`
- `rank_ast_candidates(results) -> list[RetrievalResult]`

### Storage

- `save_repository(repository) -> None`
- `save_file_metadata(file_metadata) -> None`
- `save_chunk(chunk) -> None`
- `save_structural_metadata(metadata) -> None`
- `save_bm25_text(chunk_id, bm25_text) -> None`
- `save_embedding_text(chunk_id, embedding_text) -> None`
- `save_embedding_vector(chunk_id, embedding_model, vector) -> None`
- `save_keywords(chunk_id, keywords) -> None`
- `load_chunks_for_repository(repository_id) -> list[CodeChunk]`

## Sprint 1 Definition Of Done

Sprint 1 is complete when:

- there are 10-15 prepared repositories;
- each repository has code files, 7 issues, and `.yml`;
- `schemas.py` exists;
- `data_contracts.md` exists;
- `context.md` exists;
- repository files can be loaded;
- `.yml` can be loaded, parsed, and used for filtering;
- file metadata is created;
- AST-aware chunks are created for supported languages;
- fallback chunks are created for unsupported cases;
- structural metadata is extracted where possible;
- BM25 text is created;
- BM25 top-k retrieval works;
- embedding text is created;
- chunk/query embeddings can be generated;
- dense top-k retrieval works;
- storage functions save and load core entities;
- all modules use shared schemas and contracts.

## What Is Deferred To Sprint 2

- full RRF fusion;
- final top-k evidence formatting;
- retrieval run persistence if not finished in Sprint 1;
- metrics calculation;
- experiments comparing BM25, dense, AST, and hybrid retrieval;
- issue-to-plan prompt integration;
- plan-to-code generation.

