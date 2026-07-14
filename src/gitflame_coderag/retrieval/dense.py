"""Dense retrieval interfaces owned by the embeddings workstream."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np

from gitflame_coderag.embeddings import DEFAULT_EMBEDDING_MODEL, embed_query
from gitflame_coderag.schemas import ChunkEmbedding, RetrievalResult


class DenseVectorStore(Protocol):
    def search_similar_chunks(
        self,
        query_vector: list[float],
        *,
        embedding_model: str,
        top_k: int,
        repository_id: str | None = None,
        revision: str | None = None,
    ) -> list[RetrievalResult]: ...


@dataclass
class DenseIndex:
    """Row-normalized embedding matrix for a repository revision.

    Holding vectors as one ``float32`` matrix instead of ``list[ChunkEmbedding]``
    is what makes repository-scale dense retrieval feasible: a Python
    ``list[float]`` costs ~24 KB per 768-dim vector (~12 GB at 500k chunks),
    while the same vectors cost ~1.5 GB here. Rows are L2-normalized at build
    time so a query search is a single mat-vec product.
    """

    chunk_ids: list[str]
    matrix: np.ndarray

    def __len__(self) -> int:
        return len(self.chunk_ids)


def build_dense_index(embeddings: Sequence[ChunkEmbedding]) -> DenseIndex:
    """Build a :class:`DenseIndex` from per-chunk embeddings."""
    chunk_ids = [embedding.chunk_id for embedding in embeddings]
    if not chunk_ids:
        return DenseIndex(chunk_ids=[], matrix=np.zeros((0, 0), dtype=np.float32))
    matrix = np.asarray([embedding.vector for embedding in embeddings], dtype=np.float32)
    return dense_index_from_matrix(chunk_ids, matrix)


def dense_index_from_matrix(chunk_ids: list[str], matrix: np.ndarray) -> DenseIndex:
    """Build a :class:`DenseIndex` from an already-materialized ``(n, d)`` matrix.

    The matrix is copied only when it needs normalizing or a dtype change, so
    callers that embed straight into ``float32`` avoid a second full-size array.
    """
    if len(chunk_ids) != matrix.shape[0]:
        raise ValueError(
            f"dense index needs one chunk id per row: {len(chunk_ids)} ids, {matrix.shape[0]} rows"
        )
    normalized = np.ascontiguousarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(normalized, axis=1, keepdims=True)
    # A zero vector has no direction: leave it at zero so it scores 0.0 against
    # every query, matching cosine_similarity's zero-denominator branch.
    np.divide(normalized, norms, out=normalized, where=norms > 0)
    return DenseIndex(chunk_ids=chunk_ids, matrix=normalized)


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("cosine similarity requires vectors with equal dimensions")

    a = np.asarray(vector_a, dtype=np.float32)
    b = np.asarray(vector_b, dtype=np.float32)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denominator) if denominator else 0.0


def dense_search(
    query_vector: list[float],
    embeddings: Sequence[ChunkEmbedding] | DenseIndex,
    top_k: int,
) -> list[RetrievalResult]:
    """Return the ``top_k`` chunks most similar to ``query_vector`` by cosine score.

    ``embeddings`` may be a raw ``list[ChunkEmbedding]`` or a prebuilt
    :class:`DenseIndex`. Passing the index is strongly preferred when searching
    the same repository repeatedly (e.g. once per issue), since it builds the
    normalized matrix once instead of on every call.
    """
    if top_k <= 0:
        return []

    index = embeddings if isinstance(embeddings, DenseIndex) else build_dense_index(embeddings)
    if not index.chunk_ids:
        return []

    query = np.asarray(query_vector, dtype=np.float32)
    if query.shape[0] != index.matrix.shape[1]:
        raise ValueError("cosine similarity requires vectors with equal dimensions")

    query_norm = float(np.linalg.norm(query))
    if query_norm == 0.0:
        scores = np.zeros(len(index.chunk_ids), dtype=np.float32)
    else:
        scores = index.matrix @ (query / query_norm)

    # Rank by descending score, ties broken by ascending chunk_id. lexsort applies
    # its keys last-first, so `-scores` is primary and `chunk_ids` is the tiebreak.
    order = np.lexsort((np.asarray(index.chunk_ids), -scores))[:top_k]
    return [
        RetrievalResult(
            chunk_id=index.chunk_ids[position],
            rank=rank,
            score=float(scores[position]),
            dense_score=float(scores[position]),
            source="dense",
        )
        for rank, position in enumerate(order, start=1)
    ]


def dense_retrieval_pgvector(
    query: str,
    vector_store: DenseVectorStore,
    top_k: int,
    *,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    repository_id: str | None = None,
    revision: str | None = None,
) -> list[RetrievalResult]:
    if top_k <= 0 or not query.strip():
        return []

    query_vector = embed_query(query, model_name=embedding_model)
    return vector_store.search_similar_chunks(
        query_vector,
        embedding_model=embedding_model,
        top_k=top_k,
        repository_id=repository_id,
        revision=revision,
    )


def rank_dense_results(results: list[RetrievalResult]) -> list[RetrievalResult]:
    ranked = sorted(results, key=lambda result: (-result.score, result.chunk_id))
    return [
        result.model_copy(update={"rank": rank, "source": "dense", "dense_score": result.score})
        for rank, result in enumerate(ranked, start=1)
    ]
