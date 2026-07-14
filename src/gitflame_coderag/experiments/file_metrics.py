"""File-level ranking metrics for issue-to-code experiments.

The benchmark's ground truth is ``issue.expected_files``: a handful of repository-relative
paths that the fix actually touched. Retrieval, however, ranks *chunks*. These helpers are
the single place where that gap is bridged, so every experiment runner reports numbers on
the same definition and stays comparable:

* ``recall_at_k`` / ``map_at_k`` deduplicate paths — a file found twice is found once.
* ``precision_at_k`` does not: it is chunk-level by design and answers "what share of the
  evidence we hand to the model actually comes from a file that needed changing".
* ``files_at_k`` records how many distinct files the k chunks even covered. Recall is
  capped by it, so a low ``recall_at_k`` next to a low ``files_at_k`` means the ranking
  spent its budget on one file rather than that it missed the right ones.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol


class RankedChunk(Protocol):
    """The only thing metrics need from an evidence chunk."""

    path: str


def compute_file_level_metrics(
    *,
    top_k: Sequence[RankedChunk],
    expected_files: Sequence[str],
    k_values: Sequence[int],
) -> dict[str, float]:
    expected = {path for path in expected_files if path}
    ranked_paths = [chunk.path for chunk in top_k]
    metrics: dict[str, float] = {}
    for k in k_values:
        retrieved = ranked_paths[:k]
        retrieved_set = set(retrieved)
        hits = [path for path in retrieved if path in expected]
        metrics[f"recall_at_{k}"] = (
            len(retrieved_set & expected) / len(expected) if expected else 0.0
        )
        metrics[f"precision_at_{k}"] = len(hits) / k if k > 0 else 0.0
        metrics[f"map_at_{k}"] = average_precision_at_k(retrieved, expected, k)
        metrics[f"files_at_{k}"] = float(len(retrieved_set))
    return metrics


def average_precision_at_k(ranked_paths: Sequence[str], expected: set[str], k: int) -> float:
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


def aggregate_metrics(
    issue_metrics: Sequence[dict[str, Any]],
    k_values: Sequence[int],
) -> dict[str, Any]:
    """Macro-average per-issue metrics, plus a latency distribution."""
    if not issue_metrics:
        return {"n_issues": 0}
    output: dict[str, Any] = {"n_issues": len(issue_metrics)}
    metric_names = [
        *(f"recall_at_{k}" for k in k_values),
        *(f"precision_at_{k}" for k in k_values),
        *(f"map_at_{k}" for k in k_values),
        *(f"files_at_{k}" for k in k_values),
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


def aggregate_metrics_by_config(
    issue_metrics_by_config: dict[str, list[dict[str, Any]]],
    k_values: Sequence[int],
) -> dict[str, Any]:
    return {
        config_name: aggregate_metrics(issue_metrics, k_values)
        for config_name, issue_metrics in issue_metrics_by_config.items()
    }


def percentile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    index = min(len(values) - 1, max(0, round((len(values) - 1) * q)))
    return values[index]
