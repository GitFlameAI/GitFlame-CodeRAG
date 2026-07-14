#!/usr/bin/env python3
"""Run the CodeRAG experiment matrix with original models and export one JSON file.

This script is intended for an external teammate who can run the original models locally.
It does not require Postgres: it indexes the dataset in memory, runs the required
BM25 / Dense / AST / Full RRF / Full RRF + reranker configs, computes file-level
metrics from issue.expected_files, and writes a single JSON artifact with
environment info, smoke tests, metrics, per-issue output, latency, and all errors
that happened along the way.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import traceback
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter
from typing import Any

from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.config import load_ai_config, parse_ai_config
from gitflame_coderag.embeddings import (
    describe_embedding_backend,
    embed_chunks_matrix,
    embed_query,
)
from gitflame_coderag.embeddings.service import last_encode_peak_bytes
from gitflame_coderag.experiments.file_metrics import (
    aggregate_metrics_by_config,
    compute_file_level_metrics,
)
from gitflame_coderag.experiments.validation import (
    repository_source_root,
    validate_experiment_inputs,
)
from gitflame_coderag.ingestion import filter_files_by_config, load_issues, load_repository_files
from gitflame_coderag.pipelines.retrieve_issue import build_issue_query, run_retrieval_core
from gitflame_coderag.retrieval.ast import build_ast_index
from gitflame_coderag.retrieval.bm25 import build_bm25_index
from gitflame_coderag.retrieval.dense import dense_index_from_matrix
from gitflame_coderag.schemas import EvidenceChunk, ExperimentConfig

DEFAULT_EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-base-code"
DEFAULT_RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
DEFAULT_K_VALUES = (5, 10, 15)
DEFAULT_CONFIG_NAMES = (
    "bm25_only",
    "dense_only",
    "ast_only",
    "bm25_ast",
    "bm25_dense",
    "ast_dense",
    "full_rrf",
    "full_rrf_reranker",
)


@dataclass
class ExperimentError:
    stage: str
    message: str
    repository_id: str | None = None
    issue_id: str | None = None
    error_type: str | None = None
    traceback: str | None = None


def main() -> int:
    args = parse_args()
    started_at = datetime.now(UTC)
    output_path = args.output
    errors: list[ExperimentError] = []

    result: dict[str, Any] = {
        "run_info": build_run_info(args, started_at),
        "config": build_config_summary(args),
        "experimental_pipeline": build_experimental_pipeline(args),
        "model_smoke_tests": {},
        "dataset_validation": {},
        "dataset_summary": {},
        "metrics": {},
        "per_issue_results": [],
        "errors": [],
    }

    try:
        dataset_root = args.dataset_root.resolve()
        repo_dirs = iter_repository_dirs(dataset_root)
        if args.repos:
            found = {repo.name: repo for repo in repo_dirs}
            missing = [name for name in args.repos if name not in found]
            if missing:
                raise ValueError(
                    f"repositories not found under {dataset_root}: {', '.join(missing)}"
                )
            repo_dirs = [found[name] for name in args.repos]
        stage_label = f"stage={args.stage} " if args.stage else ""
        print(
            f"{stage_label}Running {len(repo_dirs)} repositories under {dataset_root}",
            flush=True,
        )
        validation_reports = [validate_experiment_inputs(repo, args.revision) for repo in repo_dirs]
        result["dataset_validation"] = summarize_validation(validation_reports)
        validation_errors = [
            problem
            for report in validation_reports
            for problem in report.problems
            if problem.severity == "error"
        ]
        if validation_errors:
            errors.append(
                ExperimentError(
                    stage="dataset_validation",
                    message=f"Dataset validation failed with {len(validation_errors)} errors",
                )
            )
            return finish(result, errors, output_path, exit_code=1)
        print(
            f"Dataset validation OK ({result['dataset_validation']['warnings']} warnings)",
            flush=True,
        )
    except Exception as exc:  # noqa: BLE001 - always write JSON on failure
        errors.append(capture_error("dataset_validation", exc))
        return finish(result, errors, output_path, exit_code=1)

    configs = make_experiment_configs(args)
    uses_dense = any(config.use_dense for config in configs)
    uses_reranker = any(config.use_reranker for config in configs)

    reranker_model = None
    if uses_dense:
        try:
            print(f"Running embedding smoke test ({args.embedding_model})...", flush=True)
            result["model_smoke_tests"]["embedding"] = smoke_test_embedding(
                args.embedding_model,
                batch_size=args.embedding_batch_size,
            )
            embedding_smoke = result["model_smoke_tests"]["embedding"]
            print(
                f"Embedding smoke test OK (dim={embedding_smoke['embedding_dim']}, "
                f"{embedding_smoke['latency_sec']:.2f}s)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(capture_error("embedding_smoke_test", exc))
            result["model_smoke_tests"]["embedding"] = failed_smoke(exc)
            return finish(result, errors, output_path, exit_code=1)
    else:
        result["model_smoke_tests"]["embedding"] = {"ok": True, "skipped": True}

    if uses_reranker:
        try:
            print(f"Running reranker smoke test ({args.reranker_model})...", flush=True)
            reranker_model, reranker_smoke = smoke_test_reranker(
                args.reranker_model,
                device=args.reranker_device,
            )
            result["model_smoke_tests"]["reranker"] = reranker_smoke
            print(
                f"Reranker smoke test OK (load={reranker_smoke['load_latency_sec']:.2f}s, "
                f"predict={reranker_smoke['predict_latency_sec']:.2f}s)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(capture_error("reranker_smoke_test", exc))
            result["model_smoke_tests"]["reranker"] = failed_smoke(exc)
            return finish(result, errors, output_path, exit_code=1)
    else:
        result["model_smoke_tests"]["reranker"] = {"ok": True, "skipped": True}
    all_issue_metrics: dict[str, list[dict[str, Any]]] = {config.name: [] for config in configs}
    dataset_summary = {
        "repositories": 0,
        "issues": 0,
        "selected_files": 0,
        "chunks": 0,
    }

    total_repos = len(repo_dirs)
    for repo_index, repo_dir in enumerate(repo_dirs, start=1):
        repository_id = repo_dir.name
        print(f"[{repo_index}/{total_repos}] Repository {repository_id}: starting", flush=True)
        repo_started = perf_counter()
        try:
            repo_result, repo_metrics, repo_summary = run_repository_configs(
                repo_dir=repo_dir,
                repository_id=repository_id,
                revision=args.revision,
                configs=configs,
                embedding_model=args.embedding_model,
                embedding_batch_size=args.embedding_batch_size,
                attention_budget_bytes=(
                    int(args.attention_budget_gib * 1024**3)
                    if args.attention_budget_gib
                    else None
                ),
                reranker_model=reranker_model,
                k_values=args.k_values,
            )
            result["per_issue_results"].extend(repo_result)
            for config_name, metrics in repo_metrics.items():
                all_issue_metrics[config_name].extend(metrics)
            for key, value in repo_summary.items():
                dataset_summary[key] = dataset_summary.get(key, 0) + value
            print(
                f"[{repo_index}/{total_repos}] Repository {repository_id}: done in "
                f"{perf_counter() - repo_started:.2f}s "
                f"({repo_summary['issues']} issues, {repo_summary['selected_files']} files, "
                f"{repo_summary['chunks']} chunks)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[{repo_index}/{total_repos}] Repository {repository_id}: FAILED "
                f"({type(exc).__name__}: {exc})",
                flush=True,
            )
            errors.append(capture_error("repository_run", exc, repository_id=repository_id))
            if args.fail_fast:
                result["dataset_summary"] = dataset_summary
                result["metrics"] = aggregate_metrics_by_config(all_issue_metrics, args.k_values)
                return finish(result, errors, output_path, exit_code=1)

    result["dataset_summary"] = dataset_summary
    result["metrics"] = aggregate_metrics_by_config(all_issue_metrics, args.k_values)
    exit_code = 1 if errors else 0
    return finish(result, errors, output_path, exit_code=exit_code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("datasets"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/original_models_experiment_results.json"),
    )
    parser.add_argument(
        "--stage",
        default=None,
        help="Label for this run, recorded in the output JSON (e.g. large/medium/original).",
    )
    parser.add_argument(
        "--repos",
        type=parse_repo_names,
        default=None,
        help=(
            "Comma-separated repository directory names to restrict the run to. "
            "Defaults to every repository found under --dataset-root."
        ),
    )
    parser.add_argument("--revision", default="local")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--reranker-model", default=DEFAULT_RERANKER_MODEL)
    parser.add_argument("--embedding-batch-size", type=int, default=128)
    parser.add_argument("--reranker-batch-size", type=int, default=8)
    parser.add_argument("--reranker-device", default="cuda")
    parser.add_argument("--bm25-top-k", type=int, default=50)
    parser.add_argument("--dense-top-k", type=int, default=50)
    parser.add_argument("--ast-top-k", type=int, default=50)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--rrf-top-k", type=int, default=50)
    parser.add_argument("--reranker-top-k", type=int, default=50)
    parser.add_argument("--k-values", type=parse_k_values, default=DEFAULT_K_VALUES)
    parser.add_argument(
        "--configs",
        type=parse_config_names,
        default=DEFAULT_CONFIG_NAMES,
        help=(
            "Comma-separated config names: "
            "bm25_only,dense_only,ast_only,bm25_ast,bm25_dense,ast_dense,"
            "full_rrf,full_rrf_reranker"
        ),
    )
    parser.add_argument("--max-pair-chars", type=int, default=8000)
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument(
        "--attention-budget-gib",
        type=float,
        default=None,
        help=(
            "Override the peak GiB one embedding batch's attention may use. Defaults "
            "to a fraction of the GPU memory actually free at run time, which is the "
            "number that keeps long chunks from OOMing (or silently spilling into "
            "system RAM). Only set this to debug the automatic budget."
        ),
    )
    return parser.parse_args()


def parse_repo_names(raw: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    if not values:
        raise argparse.ArgumentTypeError("repos must not be empty")
    return values


def parse_k_values(raw: str) -> tuple[int, ...]:
    values = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not values or any(value <= 0 for value in values):
        raise argparse.ArgumentTypeError("k-values must be positive integers, e.g. 5,10,15")
    return values


def parse_config_names(raw: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    unknown = sorted(set(values) - set(DEFAULT_CONFIG_NAMES))
    if unknown:
        raise argparse.ArgumentTypeError(f"unknown configs: {', '.join(unknown)}")
    if not values:
        raise argparse.ArgumentTypeError("configs must not be empty")
    return values


def make_experiment_configs(args: argparse.Namespace) -> list[ExperimentConfig]:
    return [make_experiment_config(args, name) for name in args.configs]


def make_experiment_config(args: argparse.Namespace, name: str) -> ExperimentConfig:
    final_top_k = max(args.k_values)
    reranker_top_k = max(args.reranker_top_k, final_top_k)
    rrf_top_k = max(args.rrf_top_k, reranker_top_k)
    base: dict[str, Any] = {
        "name": name,
        "bm25_top_k": args.bm25_top_k,
        "dense_top_k": args.dense_top_k,
        "ast_top_k": args.ast_top_k,
        "rrf_k": args.rrf_k,
        "rrf_top_k": rrf_top_k,
        "reranker_model": args.reranker_model,
        "reranker_top_k": reranker_top_k,
        "final_top_k": final_top_k,
        "reranker_device": args.reranker_device,
        "reranker_batch_size": args.reranker_batch_size,
        "reranker_max_pair_chars": args.max_pair_chars,
        "embedding_model": args.embedding_model,
        "random_seed": 42,
    }
    config_flags = {
        "bm25_only": dict(
            use_bm25=True,
            use_dense=False,
            use_ast=False,
            use_rrf=False,
            use_reranker=False,
        ),
        "dense_only": dict(
            use_bm25=False,
            use_dense=True,
            use_ast=False,
            use_rrf=False,
            use_reranker=False,
        ),
        "ast_only": dict(
            use_bm25=False,
            use_dense=False,
            use_ast=True,
            use_rrf=False,
            use_reranker=False,
        ),
        "bm25_ast": dict(
            use_bm25=True,
            use_dense=False,
            use_ast=True,
            use_rrf=True,
            use_reranker=False,
        ),
        "bm25_dense": dict(
            use_bm25=True,
            use_dense=True,
            use_ast=False,
            use_rrf=True,
            use_reranker=False,
        ),
        "ast_dense": dict(
            use_bm25=False,
            use_dense=True,
            use_ast=True,
            use_rrf=True,
            use_reranker=False,
        ),
        "full_rrf": dict(
            use_bm25=True,
            use_dense=True,
            use_ast=True,
            use_rrf=True,
            use_reranker=False,
        ),
        "full_rrf_reranker": dict(
            use_bm25=True,
            use_dense=True,
            use_ast=True,
            use_rrf=True,
            use_reranker=True,
        ),
    }
    return ExperimentConfig(
        **base,
        **config_flags[name],
    )


def smoke_test_embedding(model_name: str, *, batch_size: int) -> dict[str, Any]:
    started = perf_counter()
    vector = embed_query(
        "def validate_reset_token(token): return token.user_id",
        model_name=model_name,
        batch_size=batch_size,
    )
    return {
        "ok": True,
        "model": model_name,
        "embedding_dim": len(vector),
        "latency_sec": perf_counter() - started,
        "first_values": vector[:5],
    }


def smoke_test_reranker(model_name: str, *, device: str) -> tuple[Any, dict[str, Any]]:
    from gitflame_coderag.retrieval.reranker import _resolve_device, load_reranker_model

    resolved_device = _resolve_device(device)
    if resolved_device != device:
        print(
            f"  reranker: requested device {device!r} is unavailable, "
            f"falling back to {resolved_device!r}",
            flush=True,
        )

    started = perf_counter()
    model = load_reranker_model(model_name, device)
    load_latency = perf_counter() - started
    if model is None:
        raise RuntimeError(
            f"Failed to load reranker model {model_name!r} on {device!r} "
            "(and cpu fallback also failed)"
        )

    query = "Fix password reset token validation bug"
    chunk = (
        "def validate_reset_token(token):\n"
        "    if token.is_expired():\n"
        "        raise InvalidTokenError()\n"
        "    return token.user_id"
    )
    predict_started = perf_counter()
    score = model.predict([(query, chunk)], batch_size=1, show_progress_bar=False)
    predict_latency = perf_counter() - predict_started
    return model, {
        "ok": True,
        "model": model_name,
        "device": resolved_device,
        "score": float(score[0]),
        "load_latency_sec": load_latency,
        "predict_latency_sec": predict_latency,
    }


def run_repository_configs(
    *,
    repo_dir: Path,
    repository_id: str,
    revision: str,
    configs: list[ExperimentConfig],
    embedding_model: str,
    embedding_batch_size: int,
    attention_budget_bytes: int | None,
    reranker_model: Any,
    k_values: tuple[int, ...],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, int]]:
    ai_config = parse_ai_config(load_ai_config(repo_dir / "repo.yml"))
    code_root = repository_source_root(repo_dir)
    files = load_repository_files(code_root, repository_id, revision)
    selected_files = filter_files_by_config(files, ai_config)
    chunks = build_chunks(selected_files, ai_config)
    total_chunks = len(chunks)
    print(
        f"  {repository_id}: {len(selected_files)} files selected, {total_chunks} chunks built",
        flush=True,
    )
    metadata_started = perf_counter()
    metadata = {}
    for chunk_index, chunk in enumerate(chunks, start=1):
        metadata[chunk.id] = extract_structural_metadata(chunk)
        if chunk_index % 20000 == 0 or chunk_index == total_chunks:
            print(
                f"    metadata [{chunk_index}/{total_chunks}] "
                f"{chunk_index / total_chunks * 100:5.1f}% | "
                f"elapsed={perf_counter() - metadata_started:.0f}s",
                flush=True,
            )

    embeddings = None
    if any(config.use_dense for config in configs):
        backend = describe_embedding_backend(embedding_model)
        budget_label = (
            f"{attention_budget_bytes / 1024**3:.2f}GiB (override)"
            if attention_budget_bytes
            else "auto (from free VRAM)"
        )
        print(
            f"  {repository_id}: embedding {total_chunks} chunks | "
            f"device={backend['device']} dtype={backend['dtype']} "
            f"max_batch_size={embedding_batch_size} attention_budget={budget_label}",
            flush=True,
        )
        embed_started = perf_counter()

        def report_embedding_progress(done: int, total: int) -> None:
            elapsed = perf_counter() - embed_started
            rate = done / elapsed if elapsed > 0 else 0.0
            remaining = total - done
            eta = remaining / rate if rate > 0 else 0.0
            print(
                f"    embed [{done}/{total}] {done / total * 100:5.1f}% | "
                f"remaining={remaining} | {rate:.0f} chunks/s | "
                f"elapsed={elapsed:.0f}s eta={eta:.0f}s",
                flush=True,
            )

        chunk_ids, matrix = embed_chunks_matrix(
            chunks,
            metadata,
            model_name=embedding_model,
            batch_size=embedding_batch_size,
            attention_budget_bytes=attention_budget_bytes,
            progress_callback=report_embedding_progress,
        )
        embeddings = dense_index_from_matrix(chunk_ids, matrix)
        print(
            f"  {repository_id}: embeddings computed in {perf_counter() - embed_started:.2f}s "
            f"({matrix.nbytes / 1e9:.2f} GB dense index, "
            f"peak {last_encode_peak_bytes() / 1024**3:.2f} GiB on GPU)",
            flush=True,
        )

    # BM25 and AST indexes depend only on the chunks, so build them once per
    # repository instead of once per issue x config (35 rebuilds at 8 configs).
    bm25_index = None
    if any(config.use_bm25 for config in configs):
        index_started = perf_counter()
        bm25_index = build_bm25_index(chunks, metadata)
        print(
            f"  {repository_id}: BM25 index over {total_chunks} chunks built in "
            f"{perf_counter() - index_started:.2f}s",
            flush=True,
        )

    ast_index = None
    if any(config.use_ast for config in configs):
        index_started = perf_counter()
        ast_index = build_ast_index(chunks, metadata)
        print(
            f"  {repository_id}: AST index over {total_chunks} chunks "
            f"({len(ast_index.postings)} terms) built in "
            f"{perf_counter() - index_started:.2f}s",
            flush=True,
        )

    issues = load_issues(repo_dir / "issues.jsonl", repository_id)
    print(
        f"  {repository_id}: running {len(issues)} issues x {len(configs)} configs",
        flush=True,
    )

    per_issue_results: list[dict[str, Any]] = []
    issue_metrics: dict[str, list[dict[str, Any]]] = {config.name: [] for config in configs}
    total_issues = len(issues)
    for issue_index, issue in enumerate(issues, start=1):
        issue_started = perf_counter()
        query_vector: list[float] | None = None
        query_embedding_latency = 0.0
        if any(config.use_dense for config in configs):
            query_embedding_started = perf_counter()
            query_vector = embed_query(
                build_issue_query(issue),
                model_name=embedding_model,
                batch_size=embedding_batch_size,
            )
            query_embedding_latency = perf_counter() - query_embedding_started
        for config in configs:
            started = perf_counter()
            evidence = run_retrieval_core(
                issue=issue,
                chunks=chunks,
                metadata_by_chunk_id=metadata,
                config=config,
                embeddings=embeddings,
                query_vector=query_vector if config.use_dense else None,
                reranker_model=reranker_model if config.use_reranker else None,
                bm25_index=bm25_index if config.use_bm25 else None,
                ast_index=ast_index if config.use_ast else None,
            )
            retrieval_latency = perf_counter() - started
            latency = retrieval_latency
            if config.use_dense:
                latency += query_embedding_latency
            top_k = [evidence_chunk_to_dict(chunk) for chunk in evidence.evidence_chunks]
            metrics = compute_file_level_metrics(
                top_k=evidence.evidence_chunks,
                expected_files=issue.expected_files,
                k_values=k_values,
            )
            metrics["latency_sec"] = latency
            issue_metrics[config.name].append(metrics)
            per_issue_results.append(
                {
                    "config_name": config.name,
                    "repository_id": repository_id,
                    "issue_id": issue.id,
                    "title": issue.title,
                    "expected_files": issue.expected_files,
                    "latency_sec": latency,
                    "retrieval_latency_sec": retrieval_latency,
                    "query_embedding_latency_sec": (
                        query_embedding_latency if config.use_dense else 0.0
                    ),
                    "metrics": metrics,
                    "warnings": [warning.model_dump(mode="json") for warning in evidence.warnings],
                    "top_k": top_k,
                }
            )
        print(
            f"    [{issue_index}/{total_issues}] issue {issue.id}: done in "
            f"{perf_counter() - issue_started:.2f}s",
            flush=True,
        )

    return (
        per_issue_results,
        issue_metrics,
        {
            "repositories": 1,
            "issues": len(issues),
            "selected_files": len(selected_files),
            "chunks": len(chunks),
        },
    )


def evidence_chunk_to_dict(chunk: EvidenceChunk) -> dict[str, Any]:
    return {
        "chunk_id": chunk.chunk_id,
        "repository_id": chunk.repository_id,
        "path": chunk.path,
        "language": chunk.language,
        "node_type": chunk.node_type,
        "symbol_name": chunk.symbol_name,
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
        "content": chunk.content,
        "scores": chunk.scores.model_dump(mode="json"),
        "source_signals": chunk.source_signals,
    }


def iter_repository_dirs(dataset_root: Path) -> list[Path]:
    return sorted(path.parent for path in dataset_root.rglob("repo.yml") if path.parent.is_dir())


def summarize_validation(reports: list[Any]) -> dict[str, Any]:
    problems = [problem for report in reports for problem in report.problems]
    return {
        "status": (
            "ok" if not any(problem.severity == "error" for problem in problems) else "failed"
        ),
        "repositories": len(reports),
        "errors": sum(1 for problem in problems if problem.severity == "error"),
        "warnings": sum(1 for problem in problems if problem.severity == "warning"),
        "details": [asdict(report) for report in reports],
    }


def build_run_info(args: argparse.Namespace, started_at: datetime) -> dict[str, Any]:
    return {
        "stage": args.stage,
        "repos": list(args.repos) if args.repos else None,
        "dataset_root": str(args.dataset_root),
        "started_at": started_at.isoformat(),
        "cwd": str(Path.cwd()),
        "git_commit": git_commit(),
        "python": sys.version,
        "platform": platform.platform(),
        "packages": package_versions(
            [
                "torch",
                "transformers",
                "sentence-transformers",
                "huggingface-hub",
                "numpy",
                "rank-bm25",
            ]
        ),
        "env": {
            "HF_TOKEN_present": bool(os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")),
            "HF_HUB_DISABLE_XET": os.getenv("HF_HUB_DISABLE_XET"),
            "TOKENIZERS_PARALLELISM": os.getenv("TOKENIZERS_PARALLELISM"),
        },
        "argv": sys.argv,
        "output": str(args.output),
    }


def build_config_summary(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "embedding_model": args.embedding_model,
        "reranker_model": args.reranker_model,
        "configs": list(args.configs),
        "experiment_configs": [
            config.model_dump(mode="json") for config in make_experiment_configs(args)
        ],
        "k_values": list(args.k_values),
        "bm25_top_k": args.bm25_top_k,
        "dense_top_k": args.dense_top_k,
        "ast_top_k": args.ast_top_k,
        "rrf_k": args.rrf_k,
        "rrf_top_k": args.rrf_top_k,
        "reranker_top_k": args.reranker_top_k,
        "embedding_batch_size": args.embedding_batch_size,
        "attention_budget_gib": args.attention_budget_gib,
        "reranker_batch_size": args.reranker_batch_size,
        "reranker_device": args.reranker_device,
        "max_pair_chars": args.max_pair_chars,
    }


def build_experimental_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "configs_run": [
            {
                "name": "bm25_only",
                "pipeline": "BM25 -> top-k evidence",
                "enabled": "bm25_only" in args.configs,
            },
            {
                "name": "dense_only",
                "pipeline": "Dense vector retrieval -> top-k evidence",
                "enabled": "dense_only" in args.configs,
            },
            {
                "name": "ast_only",
                "pipeline": "AST/symbol candidate retrieval -> top-k evidence",
                "enabled": "ast_only" in args.configs,
            },
            {
                "name": "bm25_ast",
                "pipeline": (
                    "BM25 + AST/symbol candidate retrieval -> reciprocal rank fusion -> "
                    "top-k evidence"
                ),
                "enabled": "bm25_ast" in args.configs,
            },
            {
                "name": "bm25_dense",
                "pipeline": (
                    "BM25 + Dense vector retrieval -> reciprocal rank fusion -> top-k evidence"
                ),
                "enabled": "bm25_dense" in args.configs,
            },
            {
                "name": "ast_dense",
                "pipeline": (
                    "AST/symbol candidate retrieval + Dense vector retrieval -> "
                    "reciprocal rank fusion -> top-k evidence"
                ),
                "enabled": "ast_dense" in args.configs,
            },
            {
                "name": "full_rrf",
                "pipeline": ("BM25 + Dense + AST -> reciprocal rank fusion -> top-k evidence"),
                "enabled": "full_rrf" in args.configs,
            },
            {
                "name": "full_rrf_reranker",
                "pipeline": (
                    "BM25 + Dense + AST -> reciprocal rank fusion -> "
                    "cross-encoder reranker -> top-k evidence"
                ),
                "enabled": "full_rrf_reranker" in args.configs,
            },
        ],
        "metrics": ["recall_at_k", "precision_at_k", "map_at_k", "latency_sec"],
        "k_values": list(args.k_values),
        "candidate_k": {
            "bm25_top_k": args.bm25_top_k,
            "dense_top_k": args.dense_top_k,
            "ast_top_k": args.ast_top_k,
            "rrf_k": args.rrf_k,
            "rrf_top_k": args.rrf_top_k,
            "reranker_top_k": args.reranker_top_k,
            "final_top_k": max(args.k_values),
        },
        "relevance": {
            "level": "file",
            "source": "issue.expected_files",
            "rule": (
                "An evidence chunk is relevant when its repository-relative path "
                "is listed in expected_files."
            ),
            "deduplication": (
                "Recall uses unique retrieved paths; MAP ignores repeated paths "
                "after the first hit."
            ),
        },
        "aggregation": {
            "per_issue": "Metrics are computed independently for each issue/config pair.",
            "overall": (
                "Metrics are macro-averaged across all issue/config pairs for each config."
            ),
            "latency": (
                "Per-issue retrieval latency is measured after any per-repository "
                "indexing and embedding precomputation."
            ),
        },
    }


def package_versions(package_names: list[str]) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for package_name in package_names:
        try:
            versions[package_name] = version(package_name)
        except PackageNotFoundError:
            versions[package_name] = None
    return versions


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001
        return None


def failed_smoke(exc: Exception) -> dict[str, Any]:
    return {
        "ok": False,
        "error_type": type(exc).__name__,
        "message": str(exc),
    }


def capture_error(
    stage: str,
    exc: Exception,
    *,
    repository_id: str | None = None,
    issue_id: str | None = None,
) -> ExperimentError:
    return ExperimentError(
        stage=stage,
        message=str(exc),
        repository_id=repository_id,
        issue_id=issue_id,
        error_type=type(exc).__name__,
        traceback="".join(traceback.format_exception(exc)),
    )


def finish(
    result: dict[str, Any],
    errors: list[ExperimentError],
    output_path: Path,
    *,
    exit_code: int,
) -> int:
    result["finished_at"] = datetime.now(UTC).isoformat()
    result["ok"] = exit_code == 0 and not errors
    result["errors"] = [asdict(error) for error in errors]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE {output_path}")
    if errors:
        print(f"ERRORS {len(errors)}")
        for error in errors[:5]:
            location = " ".join(
                part for part in [error.repository_id, error.issue_id] if part is not None
            )
            print(f"- {error.stage} {location}: {error.error_type}: {error.message}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
