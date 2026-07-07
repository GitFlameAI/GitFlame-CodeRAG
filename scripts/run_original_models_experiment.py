#!/usr/bin/env python3
"""Run the full CodeRAG experiment with original models and export one JSON file.

This script is intended for an external teammate who can run the original models locally.
It does not require Postgres: it indexes the dataset in memory, runs
BM25 / Dense / AST -> RRF -> reranker, computes file-level metrics from issue.expected_files,
and writes a single JSON artifact with environment info, smoke tests, metrics, per-issue output,
and all errors that happened along the way.
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
from gitflame_coderag.embeddings import embed_chunks, embed_query
from gitflame_coderag.experiments.validation import validate_dataset
from gitflame_coderag.ingestion import filter_files_by_config, load_issues, load_repository_files
from gitflame_coderag.pipelines.retrieve_issue import build_issue_query, run_retrieval_core
from gitflame_coderag.schemas import CodeChunk, EvidenceChunk, ExperimentConfig, Issue

DEFAULT_EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-base-code"
DEFAULT_RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
DEFAULT_K_VALUES = (5, 10, 15)


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
        "model_smoke_tests": {},
        "dataset_validation": {},
        "dataset_summary": {},
        "metrics": {},
        "per_issue_results": [],
        "errors": [],
    }

    try:
        dataset_root = args.dataset_root.resolve()
        validation_reports = validate_dataset(dataset_root, revision=args.revision)
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
    except Exception as exc:  # noqa: BLE001 - always write JSON on failure
        errors.append(capture_error("dataset_validation", exc))
        return finish(result, errors, output_path, exit_code=1)

    reranker_model = None
    try:
        result["model_smoke_tests"]["embedding"] = smoke_test_embedding(
            args.embedding_model,
            batch_size=args.embedding_batch_size,
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(capture_error("embedding_smoke_test", exc))
        result["model_smoke_tests"]["embedding"] = failed_smoke(exc)
        return finish(result, errors, output_path, exit_code=1)

    try:
        reranker_model, reranker_smoke = smoke_test_reranker(
            args.reranker_model,
            device=args.reranker_device,
        )
        result["model_smoke_tests"]["reranker"] = reranker_smoke
    except Exception as exc:  # noqa: BLE001
        errors.append(capture_error("reranker_smoke_test", exc))
        result["model_smoke_tests"]["reranker"] = failed_smoke(exc)
        return finish(result, errors, output_path, exit_code=1)

    config = make_experiment_config(args)
    all_issue_metrics: list[dict[str, Any]] = []
    dataset_summary = {
        "repositories": 0,
        "issues": 0,
        "selected_files": 0,
        "chunks": 0,
    }

    for repo_dir in iter_repository_dirs(args.dataset_root):
        repository_id = repo_dir.name
        try:
            repo_result, repo_metrics, repo_summary = run_repository(
                repo_dir=repo_dir,
                repository_id=repository_id,
                revision=args.revision,
                config=config,
                embedding_model=args.embedding_model,
                embedding_batch_size=args.embedding_batch_size,
                reranker_model=reranker_model,
                k_values=args.k_values,
            )
            result["per_issue_results"].extend(repo_result)
            all_issue_metrics.extend(repo_metrics)
            for key, value in repo_summary.items():
                dataset_summary[key] = dataset_summary.get(key, 0) + value
        except Exception as exc:  # noqa: BLE001
            errors.append(capture_error("repository_run", exc, repository_id=repository_id))
            if args.fail_fast:
                result["dataset_summary"] = dataset_summary
                result["metrics"] = aggregate_metrics(all_issue_metrics, args.k_values)
                return finish(result, errors, output_path, exit_code=1)

    result["dataset_summary"] = dataset_summary
    result["metrics"] = aggregate_metrics(all_issue_metrics, args.k_values)
    exit_code = 1 if errors else 0
    return finish(result, errors, output_path, exit_code=exit_code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("datasets/repositories"))
    parser.add_argument("--output", type=Path, default=Path("results/original_models_experiment_results.json"))
    parser.add_argument("--revision", default="local")
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--reranker-model", default=DEFAULT_RERANKER_MODEL)
    parser.add_argument("--embedding-batch-size", type=int, default=8)
    parser.add_argument("--reranker-batch-size", type=int, default=8)
    parser.add_argument("--reranker-device", default="cpu")
    parser.add_argument("--bm25-top-k", type=int, default=50)
    parser.add_argument("--dense-top-k", type=int, default=50)
    parser.add_argument("--ast-top-k", type=int, default=50)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--rrf-top-k", type=int, default=50)
    parser.add_argument("--reranker-top-k", type=int, default=50)
    parser.add_argument("--k-values", type=parse_k_values, default=DEFAULT_K_VALUES)
    parser.add_argument("--max-pair-chars", type=int, default=2000)
    parser.add_argument("--fail-fast", action="store_true")
    return parser.parse_args()


def parse_k_values(raw: str) -> tuple[int, ...]:
    values = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not values or any(value <= 0 for value in values):
        raise argparse.ArgumentTypeError("k-values must be positive integers, e.g. 5,10,15")
    return values


def make_experiment_config(args: argparse.Namespace) -> ExperimentConfig:
    final_top_k = max(args.k_values)
    reranker_top_k = max(args.reranker_top_k, final_top_k)
    rrf_top_k = max(args.rrf_top_k, reranker_top_k)
    return ExperimentConfig(
        name="original_models_full_rrf_reranker",
        use_bm25=True,
        use_dense=True,
        use_ast=True,
        use_rrf=True,
        use_reranker=True,
        bm25_top_k=args.bm25_top_k,
        dense_top_k=args.dense_top_k,
        ast_top_k=args.ast_top_k,
        rrf_k=args.rrf_k,
        rrf_top_k=rrf_top_k,
        reranker_model=args.reranker_model,
        reranker_top_k=reranker_top_k,
        final_top_k=final_top_k,
        reranker_device=args.reranker_device,
        reranker_batch_size=args.reranker_batch_size,
        reranker_max_pair_chars=args.max_pair_chars,
        embedding_model=args.embedding_model,
        random_seed=42,
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
    from sentence_transformers import CrossEncoder

    started = perf_counter()
    model = CrossEncoder(model_name, device=device)
    load_latency = perf_counter() - started

    query = "Fix password reset token validation bug"
    chunk = "def validate_reset_token(token):\n    if token.is_expired():\n        raise InvalidTokenError()\n    return token.user_id"
    predict_started = perf_counter()
    score = model.predict([(query, chunk)], batch_size=1, show_progress_bar=False)
    predict_latency = perf_counter() - predict_started
    return model, {
        "ok": True,
        "model": model_name,
        "device": device,
        "score": float(score[0]),
        "load_latency_sec": load_latency,
        "predict_latency_sec": predict_latency,
    }


def run_repository(
    *,
    repo_dir: Path,
    repository_id: str,
    revision: str,
    config: ExperimentConfig,
    embedding_model: str,
    embedding_batch_size: int,
    reranker_model: Any,
    k_values: tuple[int, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    ai_config = parse_ai_config(load_ai_config(repo_dir / "repo.yml"))
    code_dir = repo_dir / "code"
    files = load_repository_files(code_dir, repository_id, revision)
    selected_files = filter_files_by_config(files, ai_config)
    chunks = build_chunks(selected_files, ai_config)
    metadata = {chunk.id: extract_structural_metadata(chunk) for chunk in chunks}
    embeddings = embed_chunks(
        chunks,
        metadata,
        model_name=embedding_model,
        batch_size=embedding_batch_size,
    )
    issues = load_issues(repo_dir / "issues.jsonl", repository_id)

    per_issue_results: list[dict[str, Any]] = []
    issue_metrics: list[dict[str, Any]] = []
    for issue in issues:
        started = perf_counter()
        query_vector = embed_query(
            build_issue_query(issue),
            model_name=embedding_model,
            batch_size=embedding_batch_size,
        )
        evidence = run_retrieval_core(
            issue=issue,
            chunks=chunks,
            metadata_by_chunk_id=metadata,
            config=config,
            embeddings=embeddings,
            query_vector=query_vector,
            reranker_model=reranker_model,
        )
        latency = perf_counter() - started
        top_k = [evidence_chunk_to_dict(chunk) for chunk in evidence.evidence_chunks]
        metrics = compute_file_level_metrics(
            top_k=evidence.evidence_chunks,
            expected_files=issue.expected_files,
            k_values=k_values,
        )
        metrics["latency_sec"] = latency
        issue_metrics.append(metrics)
        per_issue_results.append(
            {
                "repository_id": repository_id,
                "issue_id": issue.id,
                "title": issue.title,
                "expected_files": issue.expected_files,
                "latency_sec": latency,
                "metrics": metrics,
                "warnings": [warning.model_dump(mode="json") for warning in evidence.warnings],
                "top_k": top_k,
            }
        )

    return per_issue_results, issue_metrics, {
        "repositories": 1,
        "issues": len(issues),
        "selected_files": len(selected_files),
        "chunks": len(chunks),
    }


def compute_file_level_metrics(
    *,
    top_k: list[EvidenceChunk],
    expected_files: list[str],
    k_values: tuple[int, ...],
) -> dict[str, float]:
    expected = {path for path in expected_files if path}
    ranked_paths = [chunk.path for chunk in top_k]
    metrics: dict[str, float] = {}
    for k in k_values:
        retrieved = ranked_paths[:k]
        retrieved_set = set(retrieved)
        hits = [path for path in retrieved if path in expected]
        metrics[f"recall_at_{k}"] = len(retrieved_set & expected) / len(expected) if expected else 0.0
        metrics[f"precision_at_{k}"] = len(hits) / k if k > 0 else 0.0
        metrics[f"map_at_{k}"] = average_precision_at_k(retrieved, expected, k)
    return metrics


def average_precision_at_k(ranked_paths: list[str], expected: set[str], k: int) -> float:
    if not expected or k <= 0:
        return 0.0
    hits = 0
    precision_sum = 0.0
    seen: set[str] = set()
    for position, path in enumerate(ranked_paths[:k], start=1):
        if path in seen:
            continue
        seen.add(path)
        if path not in expected:
            continue
        hits += 1
        precision_sum += hits / position
    return precision_sum / min(len(expected), k)


def aggregate_metrics(issue_metrics: list[dict[str, Any]], k_values: tuple[int, ...]) -> dict[str, Any]:
    if not issue_metrics:
        return {"n_issues": 0}
    output: dict[str, Any] = {"n_issues": len(issue_metrics)}
    metric_names = [
        *(f"recall_at_{k}" for k in k_values),
        *(f"precision_at_{k}" for k in k_values),
        *(f"map_at_{k}" for k in k_values),
    ]
    for name in metric_names:
        values = [float(metrics.get(name, 0.0)) for metrics in issue_metrics]
        output[name] = sum(values) / len(values)

    latencies = sorted(float(metrics["latency_sec"]) for metrics in issue_metrics)
    output["latency_avg_sec"] = sum(latencies) / len(latencies)
    output["latency_p50_sec"] = percentile(latencies, 0.50)
    output["latency_p95_sec"] = percentile(latencies, 0.95)
    output["latency_max_sec"] = max(latencies)
    return output


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    index = min(len(values) - 1, max(0, round((len(values) - 1) * q)))
    return values[index]


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
    return sorted(path for path in dataset_root.iterdir() if path.is_dir() and (path / "repo.yml").exists())


def summarize_validation(reports: list[Any]) -> dict[str, Any]:
    problems = [problem for report in reports for problem in report.problems]
    return {
        "status": "ok" if not any(problem.severity == "error" for problem in problems) else "failed",
        "repositories": len(reports),
        "errors": sum(1 for problem in problems if problem.severity == "error"),
        "warnings": sum(1 for problem in problems if problem.severity == "warning"),
        "details": [asdict(report) for report in reports],
    }


def build_run_info(args: argparse.Namespace, started_at: datetime) -> dict[str, Any]:
    return {
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
        "retrievers": ["bm25", "dense", "ast"],
        "fusion": "rrf",
        "k_values": list(args.k_values),
        "bm25_top_k": args.bm25_top_k,
        "dense_top_k": args.dense_top_k,
        "ast_top_k": args.ast_top_k,
        "rrf_k": args.rrf_k,
        "rrf_top_k": args.rrf_top_k,
        "reranker_top_k": args.reranker_top_k,
        "embedding_batch_size": args.embedding_batch_size,
        "reranker_batch_size": args.reranker_batch_size,
        "reranker_device": args.reranker_device,
        "max_pair_chars": args.max_pair_chars,
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
