# Dataset Layout

This ships **18 synthetic sample repositories** under
`datasets/repositories/<repository_id>/`, plus larger scale-test fixtures
under `datasets/medium_repositories/` and `datasets/large_repositories/`.

```text
repo_001_fastapi_blog/
  repo.yml          # repository config (follows the project template)
  issues.jsonl      # 7 GitHub-like synthetic issues
  code/             # realistic source files
    ...
```

Each `repo.yml` follows the template documented in `context.md`
(`analysis.include` / `analysis.exclude` drive file filtering).

Each issue line in `issues.jsonl` contains `id`, `title`, `body`, `labels` and
`expected_files`. `expected_chunks` is intentionally deferred beyond Sprint 1.

All code is original/synthetic and license-safe to commit; issues are marked
`source: synthetic` in each `repo.yml`.

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
| repo_016_java_spring_library | library-lending-api | java |
| repo_017_dotnet_hotel_booking | dotnet-hotel-booking | csharp |
| repo_018_ruby_rails_billing | rails-subscription-billing | ruby |

126 issues and 328 code files in total. Each repository has realistic,
distinct code (own domain, own bugs) plus real test files, so this group is
the one to use for retrieval-**quality** evaluation (recall@k, MRR, NDCG).

## Medium/large repositories (scale fixtures)

`datasets/medium_repositories/` (5 repos, 100 files each) and
`datasets/large_repositories/` (2 repos, 1000 files each) are mechanically
generated: every file is built from the same 15 rotating function templates
(`build_billing_N`, `resolve_catalog_N`, ...) with only a numeric suffix and
a `threshold` value changing. As a result:

- All 5 medium repos are byte-identical to each other (only the repo name
  and issue ids differ); both large repos are byte-identical to each other
  too. There are really only 2 unique fixtures here, each copy-pasted to hit
  a target repo count.
- The 7 issues per repo are also the same templated text, just re-ided.
- There are no cross-file imports, so AST/import-based candidate retrieval
  isn't exercised.

Use these only for scale/throughput testing (ingestion speed, index size,
retrieval latency at volume) — not as a signal for retrieval quality, since
near-identical function bodies make dense embeddings hard to tell apart.
See `datasets/dataset_overview.csv` for per-repo file/chunk/issue counts
(the `chunks` figures there are a formulaic projection, not a measured count
from the AST-aware chunker).

## Loading in code

```python
from pathlib import Path
from gitflame_coderag.config.loader import load_ai_config, parse_ai_config
from gitflame_coderag.ingestion import load_repository_files, filter_files_by_config, load_issues

repo = Path("datasets/repositories/repo_001_fastapi_blog")
config = parse_ai_config(load_ai_config(repo / "repo.yml"))
files = load_repository_files(repo / "code", "repo_001_fastapi_blog", "local")
files = filter_files_by_config(files, config)
issues = load_issues(repo / "issues.jsonl", "repo_001_fastapi_blog")
```
