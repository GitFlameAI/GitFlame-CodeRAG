"""BM25 interfaces owned by the BM25 workstream."""

from typing import Any

from gitflame_coderag.schemas import CodeChunk, RetrievalResult, StructuralMetadata


def build_bm25_text(chunk: CodeChunk, metadata: StructuralMetadata) -> str:
    raise NotImplementedError


def tokenize_for_bm25(text: str) -> list[str]:
    raise NotImplementedError


def build_bm25_index(chunks: list[CodeChunk]) -> Any:
    raise NotImplementedError


def build_bm25_query(query: str) -> str:
    raise NotImplementedError


def bm25_search(query: str, index: Any, top_k: int) -> list[RetrievalResult]:
    raise NotImplementedError


def rank_bm25_results(results: list[RetrievalResult]) -> list[RetrievalResult]:
    return sorted(results, key=lambda result: (-result.score, result.chunk_id))

