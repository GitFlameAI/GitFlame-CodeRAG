"""Structural candidate retrieval interfaces."""

from gitflame_coderag.schemas import CodeChunk, RetrievalResult, StructuralMetadata


def ast_candidate_search(
    keywords: list[str],
    chunks: list[CodeChunk],
    metadata: dict[str, StructuralMetadata],
    top_k: int,
) -> list[RetrievalResult]:
    del keywords, chunks, metadata, top_k
    raise NotImplementedError("AST candidate retrieval is assigned to the AST workstream")


def rank_ast_candidates(results: list[RetrievalResult]) -> list[RetrievalResult]:
    return sorted(results, key=lambda result: (-result.score, result.chunk_id))

