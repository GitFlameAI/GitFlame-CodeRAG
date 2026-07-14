# Dataset Layout

This ships **15 synthetic sample repositories** plus **real GitHub-style
repository fixtures** under `datasets/repositories/<repository_id>/`. The
project also uses one large external benchmark repository, Elasticsearch, for
two-stage retrieval experiments.

```text
repo_001_fastapi_blog/
  repo.yml          # repository config (follows the project template)
  issues.jsonl      # GitHub-like synthetic issues
  code/             # realistic source files
    ...
```

Each `repo.yml` follows the repository config template used by the ingestion
pipeline (`analysis.include` / `analysis.exclude` drive file filtering).

Each issue line in `issues.jsonl` contains `id`, `title`, `body`, `labels` and
`expected_files`. Relevance is evaluated at file level: an evidence chunk is
relevant when its repository-relative `path` is listed in `expected_files`.

## Repositories (small, hand/LLM-authored)

| id | name | languages |
|---|---|---|
| repo_001_fastapi_blog | fastapi-blog | python |
| repo_002_go_url_shortener | go-url-shortener | go |
| repo_003_express_todo_api | express-todo-api | javascript |
| repo_004_react_dashboard | react-metrics-dashboard | typescript |
| repo_005_flask_auth_service | flask-auth-service | python |
| repo_006_go_grpc_inventory | go-grpc-inventory | go |
| repo_007_django_shop | django-shop | python |
| repo_008_vue_notes_app | vue-notes-app | javascript/vue |
| repo_009_nestjs_payments | nestjs-payments | typescript |
| repo_010_rust_cli_tool | rust-cli-linecount | rust |
| repo_011_python_etl_pipeline | python-etl-pipeline | python |
| repo_012_node_ts_graphql | node-ts-graphql-books | typescript |
| repo_013_python_lru_cache | python-lru-cache | python |
| repo_014_python_task_queue | python-task-queue | python |
| repo_015_python_state_machine | python-state-machine | python |

These repositories are compact, domain-specific and intentionally easy to
inspect. Each repository has realistic source files, tests and synthetic
GitHub-like issues. This group is useful for debugging ingestion, filtering,
chunking, retrieval ranking and expected-file labels.

## Repositories (real / GitHub-style fixtures)

`repo_019_mkcert` through `repo_118_httparty` are larger fixtures based on real
open-source repository layouts and files. They use the same on-disk contract as
the small tier: each repository has `code/`, `repo.yml` and `issues.jsonl`.

They span far more languages than the small hand-authored tier: Go, Rust,
TypeScript/JavaScript, Ruby, Python, Java, PHP, Shell, Vue, Kotlin, C#,
C/C++, Swift and Scala. This group exercises retrieval against more realistic
naming conventions, file layouts and cross-file structure.

Issues are GitHub-like synthetic tasks with `expected_files` annotations
pointing to files under that repository's own `code/` directory.

## Medium/large scale fixtures

Earlier dataset manifests included mechanically generated `medium` and `large`
fixtures for scale and throughput testing. The current product-oriented dataset
keeps the runnable repositories under `datasets/repositories/` and uses
Elasticsearch as the main large-scale benchmark.

Use synthetic scale fixtures only for ingestion speed, index-size and latency
tests. They should not be treated as strong evidence for retrieval quality,
because repeated templates and near-identical function bodies can distort dense
retrieval behavior.

## Large external benchmark

The project also uses Elasticsearch as a large external benchmark:

| id | repository | source | use |
|---|---|---|---|
| repo_119_elasticsearch | elasticsearch | [elastic/elasticsearch](https://github.com/elastic/elasticsearch) | two-stage retrieval benchmark |

Elasticsearch is not committed under `datasets/repositories/` because of its
size.

## Dataset overview

`datasets/dataset_overview.csv` is a generated summary used for reporting. It
contains one row per local repository plus one `large_external` row for
`repo_119_elasticsearch`.

For runnable local experiments, the filesystem under `datasets/repositories/`
is the source of truth. For the external Elasticsearch row, metadata comes from
the two-stage experiment setup.

## Loading in code

```python
from pathlib import Path

from gitflame_coderag.config.loader import load_ai_config, parse_ai_config
from gitflame_coderag.ingestion import (
    filter_files_by_config,
    load_issues,
    load_repository_files,
)

repo = Path("datasets/repositories/repo_001_fastapi_blog")
config = parse_ai_config(load_ai_config(repo / "repo.yml"))
files = load_repository_files(repo / "code", "repo_001_fastapi_blog", "local")
files = filter_files_by_config(files, config)
issues = load_issues(repo / "issues.jsonl", "repo_001_fastapi_blog")
```
