#!/usr/bin/env python3
"""End-to-end demo of the two-stage retrieval pipeline for one issue.

Prints, in order: the issue, stage 1 narrowing the repository down to a handful of
candidate files (BM25 over whole files), stage 2 ranking AST chunks inside only those
files (BM25 + dense + RRF), and the final top-k evidence chunks with per-signal scores
and a code preview -- plus whether the issue's ``expected_files`` were actually found.

This calls the same production functions as ``run_two_stage_experiment.py``
(:func:`run_two_stage_retrieval` and friends); nothing about retrieval is
reimplemented here, only the terminal report around it.

Examples::

    uv run python scripts/demo_two_stage.py --list-issues
    uv run python scripts/demo_two_stage.py
    uv run python scripts/demo_two_stage.py --repo repo_022_viper --issue repo_022_issue_003
    uv run python scripts/demo_two_stage.py --pause 1.5 --no-color
"""

from __future__ import annotations

import argparse
import pickle
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

    def tqdm(iterable, *args, **kwargs):
        return iterable


from gitflame_coderag.config.loader import load_ai_config, parse_ai_config
from gitflame_coderag.embeddings import (
    DEFAULT_EMBEDDING_MODEL,
    describe_embedding_backend,
    embed_chunks_matrix,
    embed_query,
)
from gitflame_coderag.embeddings.cache import load_embedding_cache, save_embedding_cache
from gitflame_coderag.experiments.validation import repository_source_root
from gitflame_coderag.ingestion import filter_files_by_config, load_issues
from gitflame_coderag.pipelines.retrieve_issue import build_issue_query
from gitflame_coderag.pipelines.two_stage import TwoStageResult, run_two_stage_retrieval
from gitflame_coderag.retrieval.dense import dense_index_from_matrix
from gitflame_coderag.retrieval.file_level import build_file_index
from gitflame_coderag.schemas import ExperimentConfig, Issue, TwoStageConfig

try:  # Best-effort ANSI support on legacy Windows terminals; harmless if absent.
    import colorama

    colorama.just_fix_windows_console()
except ImportError:
    pass

try:  # Some Windows consoles default to a legacy codepage that can't encode "✓"/"✗".
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

import warnings

warnings.filterwarnings("ignore", message="optimum is not installed.*")

# --------------------------------------------------------------------------- rendering


class Style:
    enabled = True
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"


def paint(text: str, *codes: str) -> str:
    if not Style.enabled or not codes:
        return text
    return "".join(codes) + text + Style.RESET


def rule(title: str = "", width: int = 88) -> None:
    if not title:
        print(paint("=" * width, Style.DIM))
        return
    label = f" {title} "
    fill = max(width - len(label), 4)
    left = fill // 2
    right = fill - left
    print(paint("=" * left + label + "=" * right, Style.BOLD, Style.CYAN))


def step(tag: str, message: str) -> None:
    print(f"{paint(f'[{tag}]', Style.BOLD, Style.BLUE)} {message}")


def pause(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


def panel(title: str, body_lines: list[str], width: int = 88, color: str = Style.CYAN) -> None:
    top = f"+-- {title} " + "-" * max(width - len(title) - 5, 0)
    print(paint(top, color))
    for line in body_lines:
        for wrapped in _wrap(line, width - 2):
            print(paint("| ", color) + wrapped)
    print(paint("+" + "-" * (width - 1), color))


def _wrap(text: str, width: int) -> list[str]:
    if not text:
        return [""]
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def score_cell(value: float | None, width: int = 7) -> str:
    return " " * (width - 1) + "-" if value is None else f"{value:{width}.3f}"


# --------------------------------------------------------------------------- file cache


def get_cache_path(repository_id: str, revision: str) -> Path:
    """Get path for cached file list."""
    return Path(f"cache/files_{repository_id}_{revision}.pkl")


def _read_file_content(file_obj):
    """Read file content with proper error handling."""
    if hasattr(file_obj, "content") and file_obj.content:
        return file_obj

    # If file already has content, return as is
    if hasattr(file_obj, "content"):
        return file_obj

    try:
        with open(file_obj.path, encoding="utf-8", errors="ignore") as f:
            file_obj.content = f.read()
    except Exception:
        file_obj.content = ""
    return file_obj


def load_files_with_progress(
    code_root: Path,
    repository_id: str,
    revision: str,
    batch_size: int = 1000,
    use_cache: bool = True,
    parallel: bool = False,
    num_workers: int = 8,
) -> list:
    """Load repository files with caching and parallel processing."""
    import sys

    from gitflame_coderag.ingestion import load_repository_files

    cache_path = get_cache_path(repository_id, revision)

    # 1. Try to load from cache
    if use_cache and cache_path.exists():
        try:
            with open(cache_path, "rb") as f:
                result = pickle.load(f)
            print(f" done ({len(result)} files)", flush=True)
            return result
        except Exception as e:
            print(f" cache error: {e}, reloading...", flush=True)

    # 2. Get file list from repository
    print("          scanning repository...", end="", flush=True)
    start_time = time.perf_counter()

    # Load all files
    all_files_iter = load_repository_files(code_root, repository_id, revision)
    all_files = list(all_files_iter)
    scan_time = time.perf_counter() - start_time
    print(f" {len(all_files)} files found ({scan_time:.1f}s)", flush=True)

    # 3. Load file content (parallel or sequential)
    files_to_read = [f for f in all_files if not hasattr(f, "content") or not f.content]

    if files_to_read:
        if parallel and len(files_to_read) > 100:
            # Parallel reading
            print(
                f"          reading {len(files_to_read)} files with {num_workers} workers...",
                end="",
                flush=True,
            )
            read_start = time.perf_counter()

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(_read_file_content, f): i for i, f in enumerate(files_to_read)
                }

                # Process results with progress
                completed = 0
                for future in as_completed(future_to_file):
                    try:
                        loaded_file = future.result()
                        idx = future_to_file[future]
                        # Update the original file object
                        files_to_read[idx].content = loaded_file.content
                        completed += 1
                        if completed % 100 == 0:
                            print(
                                f"\r          reading files... {completed}/{len(files_to_read)}",
                                end="",
                                flush=True,
                            )
                    except Exception as e:
                        print(f"\n          warning: error reading file: {e}", flush=True)

            read_time = time.perf_counter() - read_start
            print(f"\r          read {len(files_to_read)} files in {read_time:.1f}s", flush=True)

        else:
            # Sequential reading with progress
            if HAS_TQDM:
                for f in tqdm(
                    files_to_read,
                    desc="Reading files",
                    unit=" files",
                    file=sys.stdout,
                    mininterval=0.5,
                ):
                    _read_file_content(f)
            else:
                print("          reading files...", end="", flush=True)
                for i, f in enumerate(files_to_read):
                    _read_file_content(f)
                    if (i + 1) % batch_size == 0:
                        print(
                            f"\r          read {min(i + 1, len(files_to_read))}/{len(files_to_read)} files...",
                            end="",
                            flush=True,
                        )
                print(f"\r          read {len(files_to_read)} files.", flush=True)

    # 4. Save to cache
    if use_cache:
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "wb") as f:
                pickle.dump(all_files, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"          cached {len(all_files)} files to {cache_path}", flush=True)
        except Exception as e:
            print(f"          cache save error: {e}", flush=True)

    return all_files


# --------------------------------------------------------------------------- pipeline


def resolve_repo_dir(dataset_root: Path, repo_name: str) -> Path:
    matches = [p.parent for p in dataset_root.rglob("repo.yml") if p.parent.name == repo_name]
    if not matches:
        available = sorted(p.parent.name for p in dataset_root.rglob("repo.yml"))
        raise SystemExit(
            f"Repository {repo_name!r} not found under {dataset_root}. "
            f"Available: {', '.join(available[:15])}{', ...' if len(available) > 15 else ''}"
        )
    return matches[0]


def pick_issue(issues: list[Issue], issue_id: str | None) -> Issue:
    if issue_id is None:
        return issues[0]
    for issue in issues:
        if issue.id == issue_id:
            return issue
    raise SystemExit(f"Issue {issue_id!r} not found. Available: {', '.join(i.id for i in issues)}")


def list_issues(repo_dir: Path, repository_id: str) -> None:
    issues = load_issues(repo_dir / "issues.jsonl", repository_id)
    rule(f"Issues in {repository_id}")
    for issue in issues:
        expected = ", ".join(issue.expected_files) or "(none)"
        print(f"  {paint(issue.id, Style.BOLD)}  {issue.title}")
        print(paint(f"      expected_files: {expected}", Style.DIM))


def build_two_stage_config(args: argparse.Namespace) -> TwoStageConfig:
    # Adjust parameters for large repos
    file_top_n = args.file_top_n
    max_chunks_per_file = args.max_chunks_per_file
    stage2_top_k = args.stage2_top_k

    if args.large_repo_mode:
        # More aggressive defaults for large repos
        file_top_n = max(file_top_n, 5)  # Narrow down stage 1 more
        max_chunks_per_file = max(1, max_chunks_per_file // 2)  # Fewer chunks per file
        stage2_top_k = min(stage2_top_k, 30)  # Smaller pool for stage 2

    stage2 = ExperimentConfig(
        name="bm25_dense_capped",
        use_bm25=True,
        use_dense=True,
        use_ast=False,
        use_rrf=True,
        use_reranker=False,
        bm25_top_k=stage2_top_k,
        dense_top_k=stage2_top_k,
        rrf_k=args.rrf_k,
        rrf_top_k=stage2_top_k,
        final_top_k=args.final_top_k,
        embedding_model=args.embedding_model,
    )
    return TwoStageConfig(
        name="demo",
        file_top_n=file_top_n,
        expand_references=args.expand_references,
        exclude_tests=True,
        max_chunks_per_file=max_chunks_per_file,
        stage2=stage2,
    )


def main() -> int:
    args = parse_args()
    Style.enabled = not args.no_color and sys.stdout.isatty()

    repo_dir = resolve_repo_dir(args.dataset_root, args.repo)
    repository_id = repo_dir.name

    if args.list_issues:
        list_issues(repo_dir, repository_id)
        return 0

    rule("GitFlame CodeRAG -- Two-Stage Retrieval Demo")
    print(f"  repository : {paint(repository_id, Style.BOLD)}  ({repo_dir})")
    print(
        f"  pipeline   : BM25 + Dense -> RRF, cap={args.max_chunks_per_file} chunks/file, no reranker"
    )
    print(f"  embedding  : {args.embedding_model}")
    print()

    # --- load issue -------------------------------------------------------
    issues = load_issues(repo_dir / "issues.jsonl", repository_id)
    issue = pick_issue(issues, args.issue)
    panel(
        f"ISSUE  {issue.id}",
        [
            paint(issue.title, Style.BOLD),
            f"labels: {', '.join(issue.labels) or '(none)'}",
            "",
            issue.body,
            "",
            f"expected file(s): {', '.join(issue.expected_files) or '(none)'}",
        ],
        color=Style.MAGENTA,
    )
    pause(args.pause)

    # --- stage 0: load + index the whole repository ------------------------
    ai_config = parse_ai_config(load_ai_config(repo_dir / "repo.yml"))
    code_root = repository_source_root(repo_dir)

    print()
    step("stage 0", "loading and indexing the repository")

    # Load files with progress and caching
    started = time.perf_counter()
    all_files = load_files_with_progress(
        code_root,
        repository_id,
        args.revision,
        use_cache=not args.no_file_cache,
        parallel=args.parallel_loading or args.large_repo_mode,
        num_workers=args.file_workers,
    )
    load_seconds = time.perf_counter() - started

    # Filter and prepare files
    started = time.perf_counter()
    selected_files = filter_files_by_config(all_files, ai_config)
    indexed_files = [f for f in selected_files if not f.metadata.is_test]
    files_by_path = {f.metadata.path: f for f in indexed_files}
    filter_seconds = time.perf_counter() - started

    print(
        f"          filtered to {len(indexed_files)} indexed files in {filter_seconds:.2f}s (loaded in {load_seconds:.1f}s)"
    )

    # Build file index
    started = time.perf_counter()
    print("          building file index...", end="", flush=True)
    file_index = build_file_index(indexed_files, build_reference_graph=args.expand_references > 0)
    index_seconds = time.perf_counter() - started
    print(f" done in {index_seconds:.2f}s")

    print(
        f"          summary: {len(all_files)} files on disk -> {len(selected_files)} selected "
        f"-> {len(indexed_files)} indexed ({len(selected_files) - len(indexed_files)} tests)"
    )
    print(f"          file index: {len(file_index.postings)} terms")
    pause(args.pause)

    # --- load the embedding model once, outside any timed section ----------
    # The first call to embed_* pays for model download/load/CUDA warmup, which has
    # nothing to do with per-query latency; done here so later timings are honest.
    print()
    step("embedding", "loading embedding model")
    started = time.perf_counter()
    print("          warming up...", end="", flush=True)
    embed_query("warmup", model_name=args.embedding_model)
    warmup_seconds = time.perf_counter() - started
    backend = describe_embedding_backend(args.embedding_model)
    print(" ready")
    print(
        f"          device: {backend['device']}, dtype: {backend['dtype']}, time: {warmup_seconds:.1f}s"
    )

    # --- issue query + dense query vector -----------------------------------
    query_text = build_issue_query(issue)
    started = time.perf_counter()
    query_vector = embed_query(query_text, model_name=args.embedding_model)
    query_embed_seconds = time.perf_counter() - started

    # --- run the actual two-stage pipeline ----------------------------------
    disk_cache = (
        None
        if args.no_embedding_cache
        else load_embedding_cache(
            args.embedding_cache_dir, repository_id, args.revision, args.embedding_model
        )
    )

    def dense_index_builder(chunks, metadata):  # noqa: ANN001 - matches DenseIndexBuilder
        cached = disk_cache or {}
        missing = [c for c in chunks if c.id not in cached]
        if missing:
            chunk_ids, matrix = embed_chunks_matrix(
                missing,
                metadata,
                model_name=args.embedding_model,
                batch_size=args.embedding_batch_size,
            )
            for chunk_id, row in zip(chunk_ids, matrix, strict=True):
                cached[chunk_id] = row
            if not args.no_embedding_cache:
                save_embedding_cache(
                    args.embedding_cache_dir,
                    repository_id,
                    args.revision,
                    args.embedding_model,
                    {chunk_id: matrix[i] for i, chunk_id in enumerate(chunk_ids)},
                )
        ids = [c.id for c in chunks]
        import numpy as np

        return dense_index_from_matrix(ids, np.asarray([cached[i] for i in ids]))

    config = build_two_stage_config(args)
    result: TwoStageResult = run_two_stage_retrieval(
        issue=issue,
        file_index=file_index,
        files_by_path=files_by_path,
        ai_config=ai_config,
        config=config,
        query_text=query_text,
        query_vector=query_vector,
        dense_index_builder=dense_index_builder,
    )

    # --- stage 1 report ------------------------------------------------------
    print()
    step(
        "stage 1",
        f"file-level BM25 narrows {len(indexed_files)} files -> "
        f"{len(result.stage1_candidates)} candidates "
        f"({result.timings.get('stage1_sec', 0.0):.3f}s)",
    )

    # Limit output for large repos
    max_display = 15 if args.large_repo_mode else 50
    candidates_to_show = result.stage1_candidates[:max_display]

    print(f"          {'rank':>4}  {'score':>7}  {'source':<10}  path")
    for candidate in candidates_to_show:
        marker = " *" if candidate.path in issue.expected_files else ""
        color = Style.GREEN if marker else Style.RESET
        print(
            paint(
                f"          {candidate.rank:>4}  {candidate.score:7.2f}  "
                f"{candidate.source:<10}  {candidate.path}{marker}",
                color,
            )
        )

    if len(result.stage1_candidates) > max_display:
        print(f"          ... and {len(result.stage1_candidates) - max_display} more files")

    found_stage1 = [p for p in issue.expected_files if p in result.candidate_paths]
    if issue.expected_files:
        verdict = (
            paint(f"expected file(s) survived stage 1: {', '.join(found_stage1)}", Style.GREEN)
            if found_stage1 == issue.expected_files
            else paint(
                f"expected file(s) MISSING from stage-1 candidates: "
                f"{', '.join(set(issue.expected_files) - set(found_stage1))}",
                Style.RED,
            )
        )
        print(f"          {verdict}")
    pause(args.pause)

    # --- stage 2 report --------------------------------------------------------
    print()
    step(
        "stage 2",
        f"chunking {len(result.stage1_candidates)} candidate files -> "
        f"{result.n_candidate_chunks} AST chunks "
        f"({result.timings.get('chunking_sec', 0.0):.3f}s)",
    )
    print(
        f"          embedding chunks + issue query with {args.embedding_model} "
        f"({result.timings.get('embedding_sec', 0.0):.2f}s chunks, "
        f"{query_embed_seconds:.2f}s query)"
    )
    print(
        f"          BM25 + Dense -> RRF fusion (rrf_k={args.rrf_k}) -> "
        f"cap {args.max_chunks_per_file} chunks/file "
        f"({result.timings.get('stage2_sec', 0.0):.3f}s)"
    )
    pause(args.pause)

    # --- final evidence ----------------------------------------------------------
    print()
    rule(f"TOP-{args.final_top_k} EVIDENCE CHUNKS")
    header = f"  {'#':>2}  {'rrf':>7}  {'bm25':>7}  {'dense':>7}  {'lines':<11}  path"
    print(paint(header, Style.BOLD))
    evidence_chunks = result.evidence.evidence_chunks
    for rank, chunk in enumerate(evidence_chunks, start=1):
        marker = " * expected" if chunk.path in issue.expected_files else ""
        color = Style.GREEN if marker else Style.RESET
        lines = f"{chunk.start_line}-{chunk.end_line}"
        symbol = f"  [{chunk.symbol_name}]" if chunk.symbol_name else ""
        print(
            paint(
                f"  {rank:>2}  {score_cell(chunk.scores.rrf)}  {score_cell(chunk.scores.bm25)}  "
                f"{score_cell(chunk.scores.dense)}  {lines:<11}  {chunk.path}{symbol}{marker}",
                color,
            )
        )
    if not evidence_chunks:
        print(paint("  (no evidence chunks returned)", Style.RED))

    found_final = {c.path for c in evidence_chunks} & set(issue.expected_files)
    if issue.expected_files:
        print()
        if found_final == set(issue.expected_files):
            print(
                paint(
                    f"  ✓ all expected files retrieved: {', '.join(sorted(found_final))}",
                    Style.GREEN,
                    Style.BOLD,
                )
            )
        else:
            missing = set(issue.expected_files) - found_final
            print(
                paint(
                    f"  ✗ missing expected file(s): {', '.join(sorted(missing))}",
                    Style.RED,
                    Style.BOLD,
                )
            )

    if evidence_chunks and args.show_content:
        # Limit detailed content display for large repos
        max_content_chunks = 3 if args.large_repo_mode else args.final_top_k

        for rank, chunk in enumerate(evidence_chunks[:max_content_chunks], start=1):
            code_lines = chunk.content.splitlines()
            preview_lines = (
                args.content_lines if not args.large_repo_mode else min(8, args.content_lines)
            )
            preview = code_lines[:preview_lines]
            symbol = f"  [{chunk.symbol_name}]" if chunk.symbol_name else ""
            body = [f"{chunk.path}:{chunk.start_line}-{chunk.end_line}  ({chunk.language}){symbol}"]
            body.append("")
            body.extend(f"{chunk.start_line + i:>5} | {line}" for i, line in enumerate(preview))
            if len(code_lines) > len(preview):
                body.append(paint(f"... {len(code_lines) - len(preview)} more lines", Style.DIM))
            marker = " -- expected" if chunk.path in issue.expected_files else ""
            color = Style.GREEN if marker else Style.YELLOW
            panel(f"EVIDENCE #{rank}{marker}", body, color=color)

        if len(evidence_chunks) > max_content_chunks:
            print(
                paint(
                    f"... {len(evidence_chunks) - max_content_chunks} more evidence chunks (use --show-content=false to hide)",
                    Style.DIM,
                )
            )

    print()
    total = sum(result.timings.values()) + query_embed_seconds
    timings = " ".join(
        f"{label}={result.timings.get(key, 0.0):.2f}s"
        for key, label in (
            ("stage1_sec", "stage1"),
            ("chunking_sec", "chunk"),
            ("embedding_sec", "embed"),
            ("stage2_sec", "stage2"),
        )
    )
    rule()
    print(f"  total wall time: {total:.2f}s   ({timings})")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dataset-root", type=Path, default=Path("datasets/big_repo"))
    parser.add_argument(
        "--repo", default="repo_119_elasticsearch", help="Repository directory name."
    )
    parser.add_argument("--issue", default=None, help="Issue id; defaults to the first issue.")
    parser.add_argument(
        "--list-issues", action="store_true", help="List issues for --repo and exit."
    )
    parser.add_argument("--revision", default="local")

    parser.add_argument(
        "--large-repo-mode",
        action="store_true",
        help="Optimize for large repositories: faster stage-1 narrowing, fewer chunks, less output.",
    )

    # File loading optimizations
    parser.add_argument(
        "--no-file-cache",
        action="store_true",
        help="Disable file cache (always reload from disk).",
    )
    parser.add_argument(
        "--parallel-loading",
        action="store_true",
        help="Enable parallel file reading (faster for large repos).",
    )
    parser.add_argument(
        "--file-workers",
        type=int,
        default=8,
        help="Number of workers for parallel file reading.",
    )

    parser.add_argument("--file-top-n", type=int, default=100, help="Stage-1 files kept.")
    parser.add_argument("--expand-references", type=int, default=0)
    parser.add_argument("--max-chunks-per-file", type=int, default=3)
    parser.add_argument(
        "--stage2-top-k", type=int, default=50, help="Stage-2 BM25/Dense/RRF pool size."
    )
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--final-top-k", type=int, default=15)

    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--embedding-batch-size", type=int, default=32)
    parser.add_argument("--embedding-cache-dir", type=Path, default=Path("cache/embeddings"))
    parser.add_argument("--no-embedding-cache", action="store_true")

    parser.add_argument("--show-content", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--content-lines", type=int, default=14)
    parser.add_argument(
        "--pause",
        type=float,
        default=0.0,
        help="Seconds to pause between sections (for recording).",
    )
    parser.add_argument("--no-color", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
