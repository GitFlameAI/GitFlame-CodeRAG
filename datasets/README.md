# Dataset Layout

Store each repository under `datasets/repositories/<repository_id>/`:

```text
repo_001_example/
  repo.yml
  issues.jsonl
  code/
    ...
```

Do not commit downloaded repository contents unless their license and project rules allow it.
Each issue must contain `id`, `title`, `body`, `labels`, and `expected_files`.
`expected_chunks` is intentionally deferred beyond Sprint 1.

