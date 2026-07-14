"""Persistent on-disk cache for chunk embeddings, keyed by chunk id + embedding model.

Chunk ids are content-derived (see ``chunking/ast_grep.py`` and ``chunking/fallback.py``),
so a vector cached under one id is valid for that exact chunk content on that model until
either changes -- nothing here needs to re-check content hashes.

One file per ``(repository_id, revision, embedding_model)`` under ``cache_dir``, holding a
``chunk_ids`` array and the matching ``(n, dim)`` float32 matrix. This is the same
representation :func:`gitflame_coderag.embeddings.embed_chunks_matrix` already returns, so
callers merge cache hits and freshly embedded chunks without a conversion step.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def cache_path(cache_dir: Path, repository_id: str, revision: str, embedding_model: str) -> Path:
    return cache_dir / _slug(embedding_model) / f"{_slug(repository_id)}__{_slug(revision)}.npz"


def load_embedding_cache(
    cache_dir: Path,
    repository_id: str,
    revision: str,
    embedding_model: str,
) -> dict[str, np.ndarray]:
    """Load cached vectors for one repository revision, or ``{}`` if none are cached yet."""
    path = cache_path(cache_dir, repository_id, revision, embedding_model)
    if not path.exists():
        return {}

    with np.load(path) as data:
        chunk_ids = data["chunk_ids"]
        matrix = data["vectors"]
    return {chunk_id: matrix[row] for row, chunk_id in enumerate(chunk_ids)}


def save_embedding_cache(
    cache_dir: Path,
    repository_id: str,
    revision: str,
    embedding_model: str,
    vectors: dict[str, np.ndarray],
) -> Path:
    """Merge ``vectors`` into the on-disk cache and write the result back atomically.

    Merges with whatever is already on disk rather than overwriting it, so calling this
    once per repository run only ever grows the cache. The write goes to a temp file first
    and is renamed into place, so a crash mid-write cannot leave a truncated cache file
    behind for the next run to load.
    """
    path = cache_path(cache_dir, repository_id, revision, embedding_model)
    if not vectors:
        return path

    merged = load_embedding_cache(cache_dir, repository_id, revision, embedding_model)
    merged.update(vectors)

    chunk_ids = np.array(sorted(merged), dtype="U")
    matrix = np.stack([merged[chunk_id] for chunk_id in chunk_ids]).astype(np.float32)

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".npz.tmp")
    # np.savez appends ".npz" to its target when given a path/string that lacks that
    # suffix, which ".npz.tmp" does -- so it's opened as a file object instead, which
    # numpy writes to as-is.
    with tmp_path.open("wb") as tmp_file:
        np.savez(tmp_file, chunk_ids=chunk_ids, vectors=matrix)
    tmp_path.replace(path)
    return path


def cache_size_bytes(cache_dir: Path, repository_id: str, revision: str, embedding_model: str) -> int:
    path = cache_path(cache_dir, repository_id, revision, embedding_model)
    return path.stat().st_size if path.exists() else 0


def _slug(value: str) -> str:
    return value.replace("/", "__").replace("\\", "__")
