#!/usr/bin/env python3
"""Run the two-stage retrieval matrix (files -> chunks) and export one JSON file.

Same dataset, same ground truth and the same file-level metrics as
``run_original_models_experiment.py``, so the two JSONs are directly comparable. The
difference is where the ranking budget is spent: stage 1 keeps ``--file-top-n`` files,
stage 2 chunks and embeds only those, and the final top-k is chunks drawn from them.

Because only the candidates are chunked, the repository is never embedded up front:
where the single-stage run embeds 361k chunks of elasticsearch, this embeds ~1.6k per
issue. ``stage1`` metrics in the output report the recall ceiling that stage 2 inherits.
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

import numpy as np

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
from gitflame_coderag.pipelines.retrieve_issue import build_issue_query
from gitflame_coderag.pipelines.two_stage import ChunkSet, run_two_stage_retrieval
from gitflame_coderag.retrieval.dense import DenseIndex, dense_index_from_matrix
from gitflame_coderag.retrieval.file_level import (
    FileIndex,
    build_file_index,
    expand_by_references,
    file_search,
)
from gitflame_coderag.schemas import (
    AIConfig,
    CodeChunk,
    EvidenceChunk,
    ExperimentConfig,
    Issue,
    RepositoryFile,
    StructuralMetadata,
    TwoStageConfig,
)

DEFAULT_EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-base-code"
DEFAULT_RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"
DEFAULT_K_VALUES = (5, 10, 15)
DEFAULT_STAGE1_N_VALUES = (10, 20, 50, 100, 200)

# Stage-2 retriever mixes. Names mirror the single-stage matrix so the two runs line up
# row by row; "*_capped" additionally limits how many chunks one file may contribute.
DEFAULT_CONFIG_NAMES = (
    "bm25_only",
    "dense_only",
    "bm25_dense",
    "full_rrf",
    "full_rrf_reranker",
    "full_rrf_reranker_capped",
)

RETRIEVER_FLAGS: dict[str, dict[str, bool]] = {
    "bm25_only": dict(use_bm25=True, use_dense=False, use_ast=False, use_rrf=False),
    "dense_only": dict(use_bm25=False, use_dense=True, use_ast=False, use_rrf=False),
    "bm25_dense": dict(use_bm25=True, use_dense=True, use_ast=False, use_rrf=True),
    "full_rrf": dict(use_bm25=True, use_dense=True, use_ast=True, use_rrf=True),
    "full_rrf_reranker": dict(use_bm25=True, use_dense=True, use_ast=True, use_rrf=True),
    "full_rrf_reranker_capped": dict(use_bm25=True, use_dense=True, use_ast=True, use_rrf=True),
}
RERANKED_CONFIGS = frozenset({"full_rrf_reranker", "full_rrf_reranker_capped"})
CAPPED_CONFIGS = frozenset({"full_rrf_reranker_capped"})


@dataclass
class ExperimentError:
    stage: str
    message: str
    repository_id: str | None = None
    issue_id: str | None = None
    error_type: str | None = None
    traceback: str | None = None


class CandidateChunkCache:
    """Chunk one issue's stage-1 candidate set once, not once per config.

    Stage 1 ignores the stage-2 flags, so all six configs of an issue narrow to exactly the
    same candidate files and would re-parse them six times — on elasticsearch that is ~27s of
    tree-sitter work per config, ~130s per repository thrown away.

    Only the most recent candidate set is held: within an issue every config asks for the
    same one, and dropping it at the issue boundary keeps a repository's worth of chunk text
    out of memory. A config with a different ``file_top_n`` simply misses and re-chunks.
    """

    def __init__(self, ai_config: AIConfig) -> None:
        self._ai_config = ai_config
        self._key: tuple[str, ...] | None = None
        self._chunk_set: ChunkSet | None = None
        self.built_sets = 0
        self.reused_sets = 0
        self.chunking_seconds = 0.0

    def build(self, files: list[RepositoryFile]) -> ChunkSet:
        key = tuple(file.metadata.path for file in files)
        if key == self._key and self._chunk_set is not None:
            self.reused_sets += 1
            return self._chunk_set

        started = perf_counter()
        chunks = build_chunks(files, self._ai_config)
        metadata = {chunk.id: extract_structural_metadata(chunk) for chunk in chunks}
        elapsed = perf_counter() - started

        # build_seconds is what this candidate set costs to chunk, and it is reported by every
        # config served from the cache: the work is shared, and charging all of it to whichever
        # config happened to run first would make the per-config latencies incomparable.
        self._key = key
        self._chunk_set = ChunkSet(chunks=chunks, metadata=metadata, build_seconds=elapsed)
        self.built_sets += 1
        self.chunking_seconds += elapsed
        return self._chunk_set


class ChunkEmbeddingCache:
    """Embed candidate chunks once per repository, not once per issue x config.

    Stage-1 candidate sets overlap heavily across issues and configs of the same
    repository, and chunk ids are content-derived, so a plain id-keyed cache turns the
    embedding cost from "per issue x config" into "per distinct chunk ever selected".
    """

    def __init__(
        self,
        *,
        model_name: str,
        batch_size: int,
        attention_budget_bytes: int | None = None,
    ) -> None:
        self._model_name = model_name
        self._batch_size = batch_size
        self._attention_budget_bytes = attention_budget_bytes
        self._vectors: dict[str, np.ndarray] = {}
        self.embedded_chunks = 0
        self.reused_chunks = 0
        self.embedding_seconds = 0.0

    def build(
        self,
        chunks: list[CodeChunk],
        metadata: dict[str, StructuralMetadata],
    ) -> DenseIndex:
        missing = [chunk for chunk in chunks if chunk.id not in self._vectors]
        self.reused_chunks += len(chunks) - len(missing)
        if missing:
            self._embed(missing, metadata)

        chunk_ids = [chunk.id for chunk in chunks]
        matrix = np.asarray([self._vectors[chunk_id] for chunk_id in chunk_ids], dtype=np.float32)
        return dense_index_from_matrix(chunk_ids, matrix)

    def _embed(
        self,
        missing: list[CodeChunk],
        metadata: dict[str, StructuralMetadata],
    ) -> None:
        backend = describe_embedding_backend(self._model_name)
        print(
            f"      embedding {len(missing)} new chunks | "
            f"device={backend['device']} dtype={backend['dtype']} "
            f"max_batch_size={self._batch_size} "
            f"attention_budget={self._budget_label()}",
            flush=True,
        )
        started = perf_counter()

        def report_progress(done: int, total: int) -> None:
            elapsed = perf_counter() - started
            rate = done / elapsed if elapsed > 0 else 0.0
            remaining = total - done
            print(
                f"        embed [{done}/{total}] {done / total * 100:5.1f}% | "
                f"remaining={remaining} | {rate:.1f} chunks/s | "
                f"elapsed={elapsed:.0f}s eta={remaining / rate if rate > 0 else 0.0:.0f}s",
                flush=True,
            )

        chunk_ids, matrix = embed_chunks_matrix(
            missing,
            metadata,
            model_name=self._model_name,
            batch_size=self._batch_size,
            attention_budget_bytes=self._attention_budget_bytes,
            progress_callback=report_progress,
        )
        for row, chunk_id in enumerate(chunk_ids):
            self._vectors[chunk_id] = matrix[row]

        elapsed = perf_counter() - started
        self.embedded_chunks += len(missing)
        self.embedding_seconds += elapsed
        print(
            f"      embedded {len(missing)} chunks in {elapsed:.1f}s "
            f"(peak {last_encode_peak_bytes() / 1024**3:.2f} GiB on GPU, "
            f"{len(self._vectors)} chunks cached)",
            flush=True,
        )

    def _budget_label(self) -> str:
        if self._attention_budget_bytes is None:
            return "auto (from free VRAM)"
        return f"{self._attention_budget_bytes / 1024**3:.2f}GiB (override)"


def main() -> int:
    args = parse_args()
    started_at = datetime.now(UTC)
    errors: list[ExperimentError] = []

    result: dict[str, Any] = {
        "run_info": build_run_info(args, started_at),
        "config": build_config_summary(args),
        "experimental_pipeline": build_experimental_pipeline(args),
        "model_smoke_tests": {},
        "dataset_validation": {},
        "dataset_summary": {},
        "stage1_metrics": {},
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
        if result["dataset_validation"]["errors"]:
            errors.append(
                ExperimentError(stage="dataset_validation", message="Dataset validation failed")
            )
            return finish(result, errors, args.output, exit_code=1)
        print(
            f"Dataset validation OK ({result['dataset_validation']['warnings']} warnings)",
            flush=True,
        )
    except Exception as exc:  # noqa: BLE001 - always write JSON on failure
        errors.append(capture_error("dataset_validation", exc))
        return finish(result, errors, args.output, exit_code=1)

    configs = make_two_stage_configs(args)

    if any(config.stage2.use_dense for config in configs):
        try:
            print(f"Running embedding smoke test ({args.embedding_model})...", flush=True)
            smoke = smoke_test_embedding(args.embedding_model, batch_size=args.embedding_batch_size)
            result["model_smoke_tests"]["embedding"] = smoke
            print(
                f"Embedding smoke test OK (dim={smoke['embedding_dim']}, "
                f"device={smoke['device']} dtype={smoke['dtype']}, "
                f"{smoke['latency_sec']:.2f}s)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(capture_error("embedding_smoke_test", exc))
            result["model_smoke_tests"]["embedding"] = failed_smoke(exc)
            return finish(result, errors, args.output, exit_code=1)
    else:
        result["model_smoke_tests"]["embedding"] = {"ok": True, "skipped": True}

    reranker_model = None
    if any(config.stage2.use_reranker for config in configs):
        try:
            print(f"Running reranker smoke test ({args.reranker_model})...", flush=True)
            reranker_model, smoke = smoke_test_reranker(
                args.reranker_model, device=args.reranker_device
            )
            result["model_smoke_tests"]["reranker"] = smoke
            print(
                f"Reranker smoke test OK (device={smoke['device']}, "
                f"load={smoke['load_latency_sec']:.2f}s, "
                f"predict={smoke['predict_latency_sec']:.2f}s)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(capture_error("reranker_smoke_test", exc))
            result["model_smoke_tests"]["reranker"] = failed_smoke(exc)
            return finish(result, errors, args.output, exit_code=1)
    else:
        result["model_smoke_tests"]["reranker"] = {"ok": True, "skipped": True}

    issue_metrics: dict[str, list[dict[str, Any]]] = {config.name: [] for config in configs}
    stage1_recalls: list[dict[str, dict[str, float]]] = []
    dataset_summary = {"repositories": 0, "issues": 0, "selected_files": 0, "indexed_files": 0}

    total_repos = len(repo_dirs)
    for repo_index, repo_dir in enumerate(repo_dirs, start=1):
        repository_id = repo_dir.name
        print(f"[{repo_index}/{total_repos}] {repository_id}: starting", flush=True)
        repo_started = perf_counter()
        try:
            repo_results, repo_metrics, repo_stage1, repo_summary = run_repository(
                repo_dir=repo_dir,
                repository_id=repository_id,
                args=args,
                configs=configs,
                reranker_model=reranker_model,
            )
            result["per_issue_results"].extend(repo_results)
            for config_name, metrics in repo_metrics.items():
                issue_metrics[config_name].extend(metrics)
            stage1_recalls.extend(repo_stage1)
            for key, value in repo_summary.items():
                dataset_summary[key] = dataset_summary.get(key, 0) + value
            print(
                f"[{repo_index}/{total_repos}] {repository_id}: done in "
                f"{perf_counter() - repo_started:.1f}s "
                f"({repo_summary['issues']} issues, {repo_summary['indexed_files']} indexed files)",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[{repo_index}/{total_repos}] {repository_id}: FAILED "
                f"({type(exc).__name__}: {exc})",
                flush=True,
            )
            errors.append(capture_error("repository_run", exc, repository_id=repository_id))
            if args.fail_fast:
                break

    result["dataset_summary"] = dataset_summary
    result["stage1_metrics"] = aggregate_stage1(
        stage1_recalls, args.stage1_n_values, args.expand_references
    )
    result["metrics"] = aggregate_metrics_by_config(issue_metrics, args.k_values)
    return finish(result, errors, args.output, exit_code=1 if errors else 0)


def smoke_test_embedding(model_name: str, *, batch_size: int) -> dict[str, Any]:
    """Load the embedding model and embed one query, so a broken model fails in seconds.

    Also the point where the model is pulled from the hub: doing it here keeps the download
    out of the middle of the first issue, where it looks like a hang.
    """
    started = perf_counter()
    vector = embed_query(
        "def validate_reset_token(token): return token.user_id",
        model_name=model_name,
        batch_size=batch_size,
    )
    backend = describe_embedding_backend(model_name)
    return {
        "ok": True,
        "model": model_name,
        "device": backend["device"],
        "dtype": backend["dtype"],
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
    return model, {
        "ok": True,
        "model": model_name,
        "device": resolved_device,
        "score": float(score[0]),
        "load_latency_sec": load_latency,
        "predict_latency_sec": perf_counter() - predict_started,
    }


def failed_smoke(exc: Exception) -> dict[str, Any]:
    return {"ok": False, "error_type": type(exc).__name__, "message": str(exc)}


def run_repository(
    *,
    repo_dir: Path,
    repository_id: str,
    args: argparse.Namespace,
    configs: list[TwoStageConfig],
    reranker_model: Any,
) -> tuple[
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    list[dict[str, dict[str, float]]],
    dict[str, int],
]:
    ai_config = parse_ai_config(load_ai_config(repo_dir / "repo.yml"))
    code_root = repository_source_root(repo_dir)

    started = perf_counter()
    files = filter_files_by_config(
        load_repository_files(code_root, repository_id, args.revision), ai_config
    )
    indexed_files = [file for file in files if not (args.exclude_tests and file.metadata.is_test)]
    files_by_path = {file.metadata.path: file for file in indexed_files}
    print(
        f"  {repository_id}: {len(files)} files selected, {len(indexed_files)} indexed "
        f"({'tests excluded' if args.exclude_tests else 'tests included'}) "
        f"in {perf_counter() - started:.1f}s",
        flush=True,
    )

    started = perf_counter()
    file_index = build_file_index(indexed_files, build_reference_graph=args.expand_references > 0)
    references = (
        f", {sum(len(row) for row in file_index.references)} reference edges"
        if args.expand_references > 0
        else ""
    )
    print(
        f"  {repository_id}: file index over {len(file_index)} files "
        f"({len(file_index.postings)} terms{references}) built in {perf_counter() - started:.1f}s",
        flush=True,
    )

    issues = load_issues(repo_dir / "issues.jsonl", repository_id)
    chunk_cache = CandidateChunkCache(ai_config)
    embedding_cache = ChunkEmbeddingCache(
        model_name=args.embedding_model,
        batch_size=args.embedding_batch_size,
        attention_budget_bytes=attention_budget_bytes(args),
    )
    print(
        f"  {repository_id}: running {len(issues)} issues x {len(configs)} configs "
        f"(stage 1 keeps top {args.file_top_n} files"
        f"{f' + {args.expand_references} by reference' if args.expand_references else ''})",
        flush=True,
    )

    per_issue_results: list[dict[str, Any]] = []
    metrics_by_config: dict[str, list[dict[str, Any]]] = {config.name: [] for config in configs}
    stage1_recalls: list[dict[str, dict[str, float]]] = []
    final_k = max(args.k_values)

    for issue_index, issue in enumerate(issues, start=1):
        issue_started = perf_counter()
        print(
            f"    [{issue_index}/{len(issues)}] {issue.id}: {len(issue.expected_files)} expected "
            f"files, running {len(configs)} configs",
            flush=True,
        )
        query_text = build_issue_query(issue)
        stage1 = stage1_recall_at_n(issue, file_index, args.stage1_n_values, args.expand_references)
        stage1_recalls.append(stage1)
        print(
            f"      stage1 ceiling: {format_recall_row(stage1['bm25'])}   (bm25 top-N)",
            flush=True,
        )
        print(
            f"      stage1 ceiling: {format_recall_row(stage1['with_references'])}   "
            f"(+{args.expand_references} by reference)",
            flush=True,
        )

        query_vector: list[float] | None = None
        query_embedding_seconds = 0.0
        if any(config.stage2.use_dense for config in configs):
            started = perf_counter()
            query_vector = embed_query(
                query_text,
                model_name=args.embedding_model,
                batch_size=args.embedding_batch_size,
            )
            query_embedding_seconds = perf_counter() - started

        for config_index, config in enumerate(configs, start=1):
            print(
                f"      [{config_index}/{len(configs)}] {config.name}: running...",
                flush=True,
            )
            started = perf_counter()
            outcome = run_two_stage_retrieval(
                issue,
                file_index=file_index,
                files_by_path=files_by_path,
                ai_config=ai_config,
                config=config,
                query_text=query_text,
                query_vector=query_vector if config.stage2.use_dense else None,
                chunk_builder=chunk_cache.build,
                dense_index_builder=embedding_cache.build if config.stage2.use_dense else None,
                reranker_model=reranker_model if config.stage2.use_reranker else None,
            )
            latency = perf_counter() - started
            if config.stage2.use_dense:
                latency += query_embedding_seconds

            metrics = compute_file_level_metrics(
                top_k=outcome.evidence.evidence_chunks,
                expected_files=issue.expected_files,
                k_values=args.k_values,
            )
            metrics["latency_sec"] = latency
            metrics_by_config[config.name].append(metrics)
            print(
                f"      [{config_index}/{len(configs)}] {config.name}: {latency:.1f}s | "
                f"{len(outcome.stage1_candidates)} files -> "
                f"{outcome.n_candidate_chunks} chunks | "
                f"{format_timings(outcome.timings)} | "
                f"recall@{final_k}={metrics[f'recall_at_{final_k}']:.2f} "
                f"files@{final_k}={metrics[f'files_at_{final_k}']:.0f}",
                flush=True,
            )
            per_issue_results.append(
                {
                    "config_name": config.name,
                    "repository_id": repository_id,
                    "issue_id": issue.id,
                    "title": issue.title,
                    "expected_files": issue.expected_files,
                    "latency_sec": latency,
                    "stage1_candidate_files": len(outcome.stage1_candidates),
                    "stage1_expanded_files": sum(
                        1 for c in outcome.stage1_candidates if c.source == "reference"
                    ),
                    "stage2_candidate_chunks": outcome.n_candidate_chunks,
                    "timings": outcome.timings,
                    "metrics": metrics,
                    "top_k": [
                        evidence_chunk_to_dict(chunk) for chunk in outcome.evidence.evidence_chunks
                    ],
                }
            )
        print(
            f"    [{issue_index}/{len(issues)}] {issue.id}: done in "
            f"{perf_counter() - issue_started:.2f}s",
            flush=True,
        )

    print(
        f"  {repository_id}: chunked {chunk_cache.built_sets} candidate sets in "
        f"{chunk_cache.chunking_seconds:.1f}s, reused {chunk_cache.reused_sets} across configs "
        f"(one parse per issue, not one per issue x config)",
        flush=True,
    )
    print(
        f"  {repository_id}: embedded {embedding_cache.embedded_chunks} distinct chunks in "
        f"{embedding_cache.embedding_seconds:.1f}s, reused {embedding_cache.reused_chunks} "
        f"from cache (single-stage would embed the whole repository)",
        flush=True,
    )
    return (
        per_issue_results,
        metrics_by_config,
        stage1_recalls,
        {
            "repositories": 1,
            "issues": len(issues),
            "selected_files": len(files),
            "indexed_files": len(indexed_files),
        },
    )


def stage1_recall_at_n(
    issue: Issue,
    file_index: FileIndex,
    n_values: tuple[int, ...],
    expand_references: int,
) -> dict[str, dict[str, float]]:
    """Recall of the expected files among the stage-1 candidates, before and after expansion.

    This is the ceiling stage 2 inherits: a file outside the candidate set cannot be
    retrieved no matter how good chunk ranking is, so a disappointing final recall should be
    read against this row first.

    Two rows, because the set stage 2 actually receives is not the BM25 top-N. ``bm25`` is
    the top-N alone; ``with_references`` adds the ``expand_references`` files those N pull in
    by symbol reference, which is the real candidate set — and the difference between the
    rows is the only honest answer to whether the expansion earns its chunks.
    """
    expected = {path for path in issue.expected_files if path}
    seeds = file_search(build_issue_query(issue), file_index, max(n_values))

    bm25: dict[str, float] = {}
    with_references: dict[str, float] = {}
    for n in n_values:
        top_n = seeds[:n]
        paths = {candidate.path for candidate in top_n}
        bm25[f"recall_at_{n}"] = recall(paths, expected)
        expanded = expand_by_references(top_n, file_index, expand_references)
        paths |= {candidate.path for candidate in expanded}
        with_references[f"recall_at_{n}"] = recall(paths, expected)

    return {"bm25": bm25, "with_references": with_references}


def recall(retrieved: set[str], expected: set[str]) -> float:
    return len(retrieved & expected) / len(expected) if expected else 0.0


def aggregate_stage1(
    recalls: list[dict[str, dict[str, float]]],
    n_values: tuple[int, ...],
    expand_references: int,
) -> dict[str, Any]:
    """Macro-average both stage-1 ceilings, and the recall the expansion adds at each N."""
    if not recalls:
        return {"n_issues": 0}

    output: dict[str, Any] = {"n_issues": len(recalls), "expand_references": expand_references}
    for row in ("bm25", "with_references"):
        output[row] = {
            f"recall_at_{n}": sum(entry[row][f"recall_at_{n}"] for entry in recalls) / len(recalls)
            for n in n_values
        }
    output["reference_gain"] = {
        f"recall_at_{n}": output["with_references"][f"recall_at_{n}"]
        - output["bm25"][f"recall_at_{n}"]
        for n in n_values
    }
    return output


def make_two_stage_configs(args: argparse.Namespace) -> list[TwoStageConfig]:
    return [make_two_stage_config(args, name) for name in args.configs]


def make_two_stage_config(args: argparse.Namespace, name: str) -> TwoStageConfig:
    final_top_k = max(args.k_values)
    stage2 = ExperimentConfig(
        name=name,
        **RETRIEVER_FLAGS[name],
        use_reranker=name in RERANKED_CONFIGS,
        bm25_top_k=args.stage2_top_k,
        dense_top_k=args.stage2_top_k,
        ast_top_k=args.stage2_top_k,
        rrf_k=args.rrf_k,
        rrf_top_k=args.stage2_top_k,
        reranker_model=args.reranker_model,
        reranker_top_k=args.stage2_top_k,
        final_top_k=final_top_k,
        reranker_device=args.reranker_device,
        reranker_batch_size=args.reranker_batch_size,
        reranker_max_pair_chars=args.max_pair_chars,
        embedding_model=args.embedding_model,
    )
    return TwoStageConfig(
        name=name,
        file_top_n=args.file_top_n,
        expand_references=args.expand_references,
        exclude_tests=args.exclude_tests,
        max_chunks_per_file=args.max_chunks_per_file if name in CAPPED_CONFIGS else None,
        stage2=stage2,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("datasets"))
    parser.add_argument("--output", type=Path, default=Path("results/two_stage.json"))
    parser.add_argument("--repos", type=parse_csv, default=None)
    parser.add_argument("--revision", default="local")
    parser.add_argument(
        "--stage",
        default=None,
        help="Label for this run, recorded in the output JSON (e.g. large/medium/original).",
    )

    parser.add_argument("--file-top-n", type=int, default=100)
    parser.add_argument("--expand-references", type=int, default=0)
    parser.add_argument("--exclude-tests", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--max-chunks-per-file", type=int, default=3)
    parser.add_argument("--stage1-n-values", type=parse_int_csv, default=DEFAULT_STAGE1_N_VALUES)

    parser.add_argument("--stage2-top-k", type=int, default=50)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--k-values", type=parse_int_csv, default=DEFAULT_K_VALUES)
    parser.add_argument("--configs", type=parse_csv, default=DEFAULT_CONFIG_NAMES)

    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--embedding-batch-size", type=int, default=128)
    parser.add_argument("--reranker-model", default=DEFAULT_RERANKER_MODEL)
    parser.add_argument("--reranker-device", default="cuda")
    parser.add_argument("--reranker-batch-size", type=int, default=32)
    parser.add_argument("--max-pair-chars", type=int, default=2000)
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

    args = parser.parse_args()
    unknown = sorted(set(args.configs) - set(RETRIEVER_FLAGS))
    if unknown:
        parser.error(f"unknown configs: {', '.join(unknown)}")
    return args


def parse_csv(raw: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in raw.split(",") if part.strip())


def parse_int_csv(raw: str) -> tuple[int, ...]:
    return tuple(int(part.strip()) for part in raw.split(",") if part.strip())


def format_recall_row(row: dict[str, float]) -> str:
    return " ".join(f"{key}={value:.2f}" for key, value in row.items())


def format_timings(timings: dict[str, float]) -> str:
    """Render one config's stage timings, so a slow row says *which* stage was slow."""
    labels = {
        "stage1_sec": "stage1",
        "chunking_sec": "chunk",
        "embedding_sec": "embed",
        "stage2_sec": "stage2",
    }
    return " ".join(
        f"{label}={timings[key]:.1f}s" for key, label in labels.items() if key in timings
    )


def attention_budget_bytes(args: argparse.Namespace) -> int | None:
    if not args.attention_budget_gib:
        return None
    return int(args.attention_budget_gib * 1024**3)


def evidence_chunk_to_dict(chunk: EvidenceChunk) -> dict[str, Any]:
    return {
        "chunk_id": chunk.chunk_id,
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
        "status": "ok" if not any(p.severity == "error" for p in problems) else "failed",
        "repositories": len(reports),
        "errors": sum(1 for p in problems if p.severity == "error"),
        "warnings": sum(1 for p in problems if p.severity == "warning"),
        "details": [asdict(report) for report in reports],
    }


def build_run_info(args: argparse.Namespace, started_at: datetime) -> dict[str, Any]:
    return {
        "pipeline": "two_stage",
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
        "file_top_n": args.file_top_n,
        "expand_references": args.expand_references,
        "exclude_tests": args.exclude_tests,
        "max_chunks_per_file": args.max_chunks_per_file,
        "stage1_n_values": list(args.stage1_n_values),
        "stage2_top_k": args.stage2_top_k,
        "rrf_k": args.rrf_k,
        "k_values": list(args.k_values),
        "embedding_model": args.embedding_model,
        "embedding_batch_size": args.embedding_batch_size,
        "attention_budget_gib": args.attention_budget_gib,
        "reranker_model": args.reranker_model,
        "reranker_device": args.reranker_device,
        "reranker_batch_size": args.reranker_batch_size,
        "max_pair_chars": args.max_pair_chars,
        "configs": [config.model_dump(mode="json") for config in make_two_stage_configs(args)],
    }


def build_experimental_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    expansion = (
        f" + {args.expand_references} files pulled in by symbol reference"
        if args.expand_references
        else ""
    )
    tests = "tests excluded" if args.exclude_tests else "tests included"
    return {
        "stage1": (f"BM25 over whole files ({tests}) -> top {args.file_top_n} files{expansion}"),
        "stage2": (
            "chunk + embed only the candidate files -> BM25/dense/AST -> RRF -> "
            "cross-encoder -> optional per-file cap -> top-k chunks"
        ),
        "metrics": ["recall_at_k", "precision_at_k", "map_at_k", "files_at_k", "latency_sec"],
        "relevance": {
            "level": "file",
            "source": "issue.expected_files",
            "rule": "An evidence chunk is relevant when its path is listed in expected_files.",
        },
    }


def package_versions(names: list[str]) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for name in names:
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    return versions


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:  # noqa: BLE001
        return None


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
    print(f"WROTE {output_path}", flush=True)
    if errors:
        print(f"ERRORS {len(errors)}", flush=True)
        for error in errors[:5]:
            location = " ".join(
                part for part in [error.repository_id, error.issue_id] if part is not None
            )
            print(f"- {error.stage} {location}: {error.error_type}: {error.message}", flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
