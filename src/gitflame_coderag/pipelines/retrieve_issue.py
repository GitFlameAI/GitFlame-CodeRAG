"""In-memory issue retrieval orchestration.

The core pipeline is deliberately storage-agnostic: callers provide already loaded
chunks, metadata, chunk embeddings and (for dense retrieval) the issue query
vector. DB-backed code should live in a thin wrapper above this module.
"""

from __future__ import annotations

import re
from uuid import uuid4

from gitflame_coderag.embeddings import embed_query
from gitflame_coderag.retrieval.ast import AstIndex, ast_candidate_search, ast_search_index
from gitflame_coderag.retrieval.bm25 import BM25Index, bm25_search, build_bm25_index
from gitflame_coderag.retrieval.dense import DenseIndex, dense_search
from gitflame_coderag.retrieval.evidence import build_evidence_chunks
from gitflame_coderag.retrieval.reranker import CrossEncoderLike, rerank_candidates
from gitflame_coderag.retrieval.rrf import rrf_fusion
from gitflame_coderag.schemas import (
    ChunkEmbedding,
    CodeChunk,
    EvidenceBuildResult,
    EvidenceChunk,
    ExperimentConfig,
    Issue,
    RetrievalPipelineResult,
    RetrievalResult,
    RetrievalRun,
    StructuralMetadata,
)
from gitflame_coderag.storage.repository import CodeRAGRepository

ISSUE_KEYWORD_PATTERN = re.compile(r"[A-Za-z0-9_]+")


def build_issue_query(issue: Issue) -> str:
    labels = " ".join(issue.labels)
    return "\n".join(part for part in (issue.title, issue.body, labels) if part).strip()


def build_issue_keywords(issue: Issue) -> list[str]:
    """Extract lightweight issue keywords for AST/symbol retrieval."""
    query = build_issue_query(issue)
    return ISSUE_KEYWORD_PATTERN.findall(query)


def run_retrieval_core(
    issue: Issue,
    chunks: list[CodeChunk],
    metadata_by_chunk_id: dict[str, StructuralMetadata],
    config: ExperimentConfig,
    *,
    embeddings: list[ChunkEmbedding] | DenseIndex | None = None,
    query_vector: list[float] | None = None,
    reranker_model: CrossEncoderLike | None = None,
    bm25_index: BM25Index | None = None,
    ast_index: AstIndex | None = None,
) -> EvidenceBuildResult:
    """Run BM25/Dense/AST retrieval, optional RRF, optional reranker, and evidence build.

    Dense retrieval expects a precomputed ``query_vector``. This keeps the core
    pipeline pure and testable; DB/experiment wrappers can decide how to embed the
    issue query and which embedding model to use.

    ``bm25_index``, ``ast_index`` and a :class:`DenseIndex` for ``embeddings`` are
    optional prebuilt indexes. They are derived purely from ``chunks`` and their
    metadata, so a caller running many issues against one repository should build
    them once and pass them in; otherwise every call re-indexes the whole
    repository, which dominates runtime at scale.
    """
    candidates = rank_issue_candidates(
        issue=issue,
        chunks=chunks,
        metadata_by_chunk_id=metadata_by_chunk_id,
        config=config,
        embeddings=embeddings,
        query_vector=query_vector,
        reranker_model=reranker_model,
        bm25_index=bm25_index,
        ast_index=ast_index,
    )

    return build_evidence_chunks(
        candidates,
        {chunk.id: chunk for chunk in chunks},
        top_k=config.final_top_k,
    )


def rank_issue_candidates(
    issue: Issue,
    chunks: list[CodeChunk],
    metadata_by_chunk_id: dict[str, StructuralMetadata],
    config: ExperimentConfig,
    *,
    embeddings: list[ChunkEmbedding] | DenseIndex | None = None,
    query_vector: list[float] | None = None,
    reranker_model: CrossEncoderLike | None = None,
    bm25_index: BM25Index | None = None,
    ast_index: AstIndex | None = None,
    top_k: int | None = None,
) -> list[RetrievalResult]:
    """Rank chunks for ``issue`` and stop before the evidence cut.

    ``top_k`` defaults to ``config.final_top_k`` — the list :func:`run_retrieval_core` turns
    into evidence. A caller that filters the ranking afterwards (a per-file cap, say) must
    ask for a deeper list, or the slots it frees have nothing left to refill them with.
    """
    rankings = _collect_enabled_rankings(
        issue=issue,
        chunks=chunks,
        metadata_by_chunk_id=metadata_by_chunk_id,
        config=config,
        embeddings=embeddings,
        query_vector=query_vector,
        bm25_index=bm25_index,
        ast_index=ast_index,
    )
    return _finalize_candidates(
        issue=issue,
        chunks=chunks,
        rankings=rankings,
        config=config,
        reranker_model=reranker_model,
        top_k=top_k if top_k is not None else config.final_top_k,
    )


def run_retrieval_from_db(
    repository: CodeRAGRepository,
    *,
    issue_id: str,
    repository_id: str,
    revision: str,
    config: ExperimentConfig,
    reranker_model: CrossEncoderLike | None = None,
    retrieval_run_id: str | None = None,
    experiment_run_id: str | None = None,
) -> RetrievalPipelineResult:
    """Run DB-backed retrieval and persist the retrieval run/results.

    ``experiment_run_id`` is kept for Sprint 2 experiment tracking. For production,
    this field should be removed from the retrieval path or moved behind a separate
    experiment-only storage adapter.
    """
    issue = repository.load_issue(issue_id)
    if issue is None:
        raise ValueError(f"Issue not found: {issue_id}")
    if issue.repository_id != repository_id:
        raise ValueError(
            f"Issue {issue_id} belongs to repository {issue.repository_id}, "
            f"not {repository_id}"
        )

    bundle = repository.load_repository_bundle(
        repository_id,
        revision,
        embedding_model=config.embedding_model if config.use_dense else None,
    )

    query_vector: list[float] | None = None
    if config.use_dense:
        if not bundle.embeddings:
            raise ValueError(
                "Dense retrieval requires chunk embeddings for "
                f"repository={repository_id}, revision={revision}, "
                f"embedding_model={config.embedding_model}"
            )
        query_vector = embed_query(
            build_issue_query(issue),
            model_name=config.embedding_model,
        )

    rankings = _collect_enabled_rankings(
        issue=issue,
        chunks=bundle.chunks,
        metadata_by_chunk_id=bundle.metadata,
        config=config,
        embeddings=bundle.embeddings,
        query_vector=query_vector,
    )
    final_results = _finalize_candidates(
        issue=issue,
        chunks=bundle.chunks,
        rankings=rankings,
        config=config,
        reranker_model=reranker_model,
    )
    evidence = build_evidence_chunks(
        final_results,
        {chunk.id: chunk for chunk in bundle.chunks},
        top_k=config.final_top_k,
    )

    run_id = retrieval_run_id or f"retrieval_{uuid4().hex}"
    repository.save_retrieval_run(
        RetrievalRun(
            id=run_id,
            repository_id=repository_id,
            issue_id=issue_id,
            query_text=build_issue_query(issue),
            query_keywords=build_issue_keywords(issue),
            top_k=config.final_top_k,
            retrieval_config=config.model_dump(mode="json"),
            experiment_run_id=experiment_run_id,
        )
    )
    repository.save_retrieval_results(run_id, final_results)

    return RetrievalPipelineResult(
        retrieval_run_id=run_id,
        evidence=evidence,
        results=final_results,
    )


def retrieve_issue_evidence(
    issue: Issue,
    chunks: list[CodeChunk],
    metadata_by_chunk_id: dict[str, StructuralMetadata],
    config: ExperimentConfig,
    *,
    embeddings: list[ChunkEmbedding] | None = None,
    query_vector: list[float] | None = None,
    reranker_model: CrossEncoderLike | None = None,
) -> list[EvidenceChunk]:
    """Backward-compatible convenience wrapper returning only evidence chunks."""
    result = run_retrieval_core(
        issue=issue,
        chunks=chunks,
        metadata_by_chunk_id=metadata_by_chunk_id,
        config=config,
        embeddings=embeddings,
        query_vector=query_vector,
        reranker_model=reranker_model,
    )
    return result.evidence_chunks


def _collect_enabled_rankings(
    *,
    issue: Issue,
    chunks: list[CodeChunk],
    metadata_by_chunk_id: dict[str, StructuralMetadata],
    config: ExperimentConfig,
    embeddings: list[ChunkEmbedding] | DenseIndex | None,
    query_vector: list[float] | None,
    bm25_index: BM25Index | None = None,
    ast_index: AstIndex | None = None,
) -> list[list[RetrievalResult]]:
    rankings: list[list[RetrievalResult]] = []

    if config.use_bm25:
        index = (
            bm25_index
            if bm25_index is not None
            else build_bm25_index(chunks, metadata_by_chunk_id)
        )
        rankings.append(bm25_search(build_issue_query(issue), index, config.bm25_top_k))

    if config.use_dense:
        if query_vector is None:
            raise ValueError("Dense retrieval requires a precomputed query_vector")
        if embeddings is None:
            raise ValueError("Dense retrieval requires chunk embeddings")
        rankings.append(dense_search(query_vector, embeddings, config.dense_top_k))

    if config.use_ast:
        if ast_index is not None:
            rankings.append(
                ast_search_index(build_issue_keywords(issue), ast_index, config.ast_top_k)
            )
        else:
            rankings.append(
                ast_candidate_search(
                    build_issue_keywords(issue),
                    chunks,
                    metadata_by_chunk_id,
                    config.ast_top_k,
                )
            )

    return [ranking for ranking in rankings if ranking]


def _combine_rankings(
    rankings: list[list[RetrievalResult]],
    config: ExperimentConfig,
) -> list[RetrievalResult]:
    if not rankings:
        return []
    if config.use_rrf:
        return rrf_fusion(rankings, top_k=config.rrf_top_k, rrf_k=config.rrf_k)
    if len(rankings) == 1:
        return rankings[0]
    raise ValueError("Multiple retrieval rankings require RRF fusion")


def _finalize_candidates(
    *,
    issue: Issue,
    chunks: list[CodeChunk],
    rankings: list[list[RetrievalResult]],
    config: ExperimentConfig,
    reranker_model: CrossEncoderLike | None,
    top_k: int | None = None,
) -> list[RetrievalResult]:
    """``top_k=None`` keeps the whole ranked pool (what the DB path persists)."""
    candidates = _combine_rankings(rankings, config)
    if not (config.use_reranker and candidates):
        return candidates if top_k is None else candidates[:top_k]

    return rerank_candidates(
        query=build_issue_query(issue),
        candidates=candidates[: config.reranker_top_k],
        chunks_by_id={chunk.id: chunk for chunk in chunks},
        model=reranker_model,
        top_k=top_k if top_k is not None else len(candidates),
        model_name=config.reranker_model,
        device=config.reranker_device,
        batch_size=config.reranker_batch_size,
        max_pair_chars=config.reranker_max_pair_chars,
    )
