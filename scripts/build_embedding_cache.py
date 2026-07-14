#!/usr/bin/env python3
"""Pre-embed every AST chunk of one or more dataset repositories into the on-disk cache.

This chunks each repository the same way the experiment scripts do (``build_chunks``,
ast-aware with fixed-window fallback), embeds whatever isn't already cached, and writes
the vectors to ``--cache-dir`` keyed by ``(repository_id, revision, embedding_model)``.
Chunk ids are content-derived, so it does not matter which subset of a repository's chunks
a later run's stage 1 selects -- ``run_two_stage_experiment.py --embedding-cache-dir`` will
hit this cache for any chunk warmed here, as long as ``--cache-dir`` points at the same
directory and both runs use the same ``--embedding-model``.

Safe to re-run: chunks already on disk are skipped, so interrupting a run and restarting it
only re-embeds whatever wasn't finished.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from time import perf_counter

from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.config import load_ai_config, parse_ai_config
from gitflame_coderag.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    describe_embedding_backend,
    embed_chunks_matrix,
    load_embedding_cache,
    save_embedding_cache,
)
from gitflame_coderag.embeddings.service import last_encode_peak_bytes
from gitflame_coderag.experiments.validation import repository_source_root
from gitflame_coderag.ingestion import filter_files_by_config, load_repository_files

DEFAULT_CACHE_DIR = Path("cache/embeddings")


def main() -> int:
    args = parse_args()
    repo_dirs = iter_repository_dirs(args.dataset_root)
    if args.repos:
        found = {repo.name: repo for repo in repo_dirs}
        missing = [name for name in args.repos if name not in found]
        if missing:
            raise SystemExit(
                f"repositories not found under {args.dataset_root}: {', '.join(missing)}"
            )
        repo_dirs = [found[name] for name in args.repos]

    backend = describe_embedding_backend(args.embedding_model)
    print(
        f"Warming embedding cache for {len(repo_dirs)} repositories -> {args.cache_dir} "
        f"(model={args.embedding_model}, device={backend['device']}, dtype={backend['dtype']})",
        flush=True,
    )

    total_embedded = 0
    total_reused = 0
    failures: list[str] = []
    for repo_index, repo_dir in enumerate(repo_dirs, start=1):
        repository_id = repo_dir.name
        started = perf_counter()
        try:
            embedded, reused = warm_repository(
                repo_dir=repo_dir,
                repository_id=repository_id,
                revision=args.revision,
                embedding_model=args.embedding_model,
                batch_size=args.embedding_batch_size,
                exclude_tests=args.exclude_tests,
                cache_dir=args.cache_dir,
                attention_budget_bytes=attention_budget_bytes(args),
            )
        except Exception as exc:  # noqa: BLE001 - keep warming the rest of the dataset
            print(f"[{repo_index}/{len(repo_dirs)}] {repository_id}: FAILED ({exc})", flush=True)
            failures.append(repository_id)
            if args.fail_fast:
                raise
            continue

        total_embedded += embedded
        total_reused += reused
        print(
            f"[{repo_index}/{len(repo_dirs)}] {repository_id}: {embedded} embedded, "
            f"{reused} already cached, done in {perf_counter() - started:.1f}s",
            flush=True,
        )

    print(
        f"Done. {total_embedded} chunks newly embedded, {total_reused} already cached, "
        f"{len(failures)} repositories failed.",
        flush=True,
    )
    return 1 if failures else 0


def warm_repository(
    *,
    repo_dir: Path,
    repository_id: str,
    revision: str,
    embedding_model: str,
    batch_size: int,
    exclude_tests: bool,
    cache_dir: Path,
    attention_budget_bytes: int | None,
) -> tuple[int, int]:
    """Embed every AST chunk of one repository not already in the cache. Returns
    ``(newly_embedded, already_cached)``."""
    ai_config = parse_ai_config(load_ai_config(repo_dir / "repo.yml"))
    code_root = repository_source_root(repo_dir)
    files = filter_files_by_config(
        load_repository_files(code_root, repository_id, revision), ai_config
    )
    if exclude_tests:
        files = [file for file in files if not file.metadata.is_test]

    chunks = build_chunks(files, ai_config)
    metadata = {chunk.id: extract_structural_metadata(chunk) for chunk in chunks}
    print(f"  {repository_id}: {len(files)} files -> {len(chunks)} AST chunks", flush=True)

    cached = load_embedding_cache(cache_dir, repository_id, revision, embedding_model)
    missing = [chunk for chunk in chunks if chunk.id not in cached]
    reused_count = len(chunks) - len(missing)
    if not missing:
        print(f"  {repository_id}: all {reused_count} chunks already cached, nothing to do", flush=True)
        return 0, reused_count

    print(
        f"  {repository_id}: embedding {len(missing)} new chunks ({reused_count} already cached)",
        flush=True,
    )
    embed_started = perf_counter()

    def report_progress(done: int, total: int) -> None:
        elapsed = perf_counter() - embed_started
        rate = done / elapsed if elapsed > 0 else 0.0
        remaining = total - done
        eta = remaining / rate if rate > 0 else 0.0
        print(
            f"    embed [{done}/{total}] {done / total * 100:5.1f}% | "
            f"{rate:.1f} chunks/s | elapsed={elapsed:.0f}s eta={eta:.0f}s",
            flush=True,
        )

    chunk_ids, matrix = embed_chunks_matrix(
        missing,
        metadata,
        model_name=embedding_model,
        batch_size=batch_size,
        attention_budget_bytes=attention_budget_bytes,
        progress_callback=report_progress,
    )
    new_vectors = {chunk_id: matrix[row] for row, chunk_id in enumerate(chunk_ids)}
    path = save_embedding_cache(cache_dir, repository_id, revision, embedding_model, new_vectors)
    print(
        f"  {repository_id}: embedded {len(new_vectors)} chunks in "
        f"{perf_counter() - embed_started:.1f}s (peak {last_encode_peak_bytes() / 1024**3:.2f} GiB "
        f"on GPU), saved to {path}",
        flush=True,
    )
    return len(new_vectors), reused_count


def iter_repository_dirs(dataset_root: Path) -> list[Path]:
    return sorted(path.parent for path in dataset_root.rglob("repo.yml") if path.parent.is_dir())


def attention_budget_bytes(args: argparse.Namespace) -> int | None:
    if not args.attention_budget_gib:
        return None
    return int(args.attention_budget_gib * 1024**3)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("datasets"))
    parser.add_argument("--repos", type=parse_csv, default=None)
    parser.add_argument("--revision", default="local")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--embedding-batch-size", type=int, default=128)
    parser.add_argument("--exclude-tests", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--attention-budget-gib",
        type=float,
        default=None,
        help="Override the peak GiB one embedding batch's attention may use (see the "
        "same flag on run_two_stage_experiment.py). Defaults to a fraction of free VRAM.",
    )
    return parser.parse_args()


def parse_csv(raw: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in raw.split(",") if part.strip())


if __name__ == "__main__":
    raise SystemExit(main())
