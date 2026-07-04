"""Build the unified experiment manifest for Sprint 2.

Owner: Kirill. Scans ``datasets/repositories/``, runs lightweight validation of
each repository bundle (config, code, issues, expected_files, revision) and writes
``experiment_manifest.yml`` - a single reproducible description of every
experiment input plus the experiment matrix and hyperparameter grid.

Standalone: depends only on the Python standard library and PyYAML, so it runs in
CI or on any teammate's machine without installing the full package. The
authoritative, schema-aware validator lives in
``gitflame_coderag.experiments.validate_experiment_inputs``.

Usage:
    python scripts/build_manifest.py [--revision local] [--out experiment_manifest.yml]
"""

from __future__ import annotations

import argparse
import json
import re
from functools import lru_cache
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = REPO_ROOT / "datasets" / "repositories"

# Experiment matrix and hyperparameter grid (Sprint 2 scope, see Sprint_2 brief).
EXPERIMENT = {
    "retrievers": ["bm25", "dense", "ast"],
    "fusion": "rrf",
    "reranker": {"enabled": True, "fallback": True},
    "ablations": ["bm25", "dense", "ast", "rrf", "rrf_reranker"],
    "metrics": ["recall_at_k", "mrr", "map", "ndcg_at_k"],
    "k_values": [1, 3, 5, 10],
    "hyperparameters": {
        "bm25_top_k": [50, 100],
        "dense_top_k": [50, 100],
        "ast_top_k": [20, 50],
        "rrf_k": [60],
        "reranker_top_k": [20, 50],
        "final_top_k": [5, 10],
    },
}


@lru_cache(maxsize=512)
def _compile_glob(pattern: str) -> re.Pattern[str]:
    i, n = 0, len(pattern)
    out = ["^"]
    while i < n:
        c = pattern[i]
        if c == "*":
            if pattern[i : i + 2] == "**":
                if pattern[i : i + 3] == "**/":
                    out.append("(?:.*/)?")
                    i += 3
                    continue
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def _matches(path: str, pattern: str) -> bool:
    if _compile_glob(pattern).match(path):
        return True
    if "/" not in pattern:
        return bool(_compile_glob(pattern).match(path.rsplit("/", 1)[-1]))
    return False


def _selected(paths: list[str], include: list[str], exclude: list[str]) -> set[str]:
    inc = include or ["**/*"]
    return {
        p
        for p in paths
        if any(_matches(p, q) for q in inc) and not any(_matches(p, q) for q in exclude)
    }


def _repo_entry(repo_dir: Path, revision: str) -> dict:
    config = yaml.safe_load((repo_dir / "repo.yml").read_text(encoding="utf-8"))
    analysis = config.get("analysis") or {}
    include = analysis.get("include") or ["**/*"]
    exclude = analysis.get("exclude") or []
    languages = (config.get("repository") or {}).get("language_priority") or []

    code_dir = repo_dir / "code"
    paths = sorted(
        p.relative_to(code_dir).as_posix() for p in code_dir.rglob("*") if p.is_file()
    )
    selected = _selected(paths, include, exclude)

    issues = [
        json.loads(line)
        for line in (repo_dir / "issues.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_total = expected_missing = expected_excluded = 0
    problems: list[str] = []
    for issue in issues:
        for exp in issue.get("expected_files", []):
            expected_total += 1
            if exp not in paths:
                expected_missing += 1
                problems.append(f"{issue.get('id')}: missing expected_file {exp}")
            elif exp not in selected:
                expected_excluded += 1
                problems.append(f"{issue.get('id')}: expected_file excluded {exp}")

    rel = repo_dir.relative_to(REPO_ROOT).as_posix()
    valid = expected_missing == 0 and bool(paths) and bool(selected) and len(issues) == 7
    return {
        "repository_id": repo_dir.name,
        "name": (config.get("repository") or {}).get("name", repo_dir.name),
        "revision": revision,
        "languages": languages,
        "config": f"{rel}/repo.yml",
        "code_path": f"{rel}/code",
        "issues_path": f"{rel}/issues.jsonl",
        "n_code_files": len(paths),
        "n_selected_files": len(selected),
        "n_issues": len(issues),
        "expected_files_total": expected_total,
        "expected_files_missing": expected_missing,
        "expected_files_excluded": expected_excluded,
        "valid": valid,
        "problems": problems,
    }


def build_manifest(dataset_root: Path, revision: str) -> dict:
    repos = sorted(
        p for p in dataset_root.iterdir() if p.is_dir() and (p / "repo.yml").exists()
    )
    entries = [_repo_entry(r, revision) for r in repos]
    languages: dict[str, int] = {}
    for e in entries:
        for lang in e["languages"]:
            languages[lang] = languages.get(lang, 0) + 1
    n_errors = sum(len(e["problems"]) for e in entries)
    return {
        "version": 1,
        "dataset": {
            "root": dataset_root.relative_to(REPO_ROOT).as_posix(),
            "revision": revision,
            "n_repositories": len(entries),
            "n_code_files": sum(e["n_code_files"] for e in entries),
            "n_issues": sum(e["n_issues"] for e in entries),
            "n_expected_files": sum(e["expected_files_total"] for e in entries),
            "languages": dict(sorted(languages.items())),
        },
        "experiment": EXPERIMENT,
        "validation": {
            "status": "ok" if n_errors == 0 else "failed",
            "problems": n_errors,
            "all_valid": all(e["valid"] for e in entries),
        },
        "repositories": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build experiment_manifest.yml")
    parser.add_argument("--revision", default="local")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "experiment_manifest.yml")
    args = parser.parse_args()

    manifest = build_manifest(DATASET_ROOT, args.revision)
    header = (
        "# Auto-generated by scripts/build_manifest.py - do not edit by hand.\n"
        "# Unified experiment manifest for the Sprint 2 GitFlame CodeRAG pipeline.\n"
    )
    args.out.write_text(
        header + yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    v = manifest["validation"]
    d = manifest["dataset"]
    print(f"Wrote {args.out.relative_to(REPO_ROOT)}")
    print(f"  repositories: {d['n_repositories']}, issues: {d['n_issues']}, "
          f"expected_files: {d['n_expected_files']}")
    print(f"  validation: {v['status']} ({v['problems']} problems)")
    return 0 if v["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
