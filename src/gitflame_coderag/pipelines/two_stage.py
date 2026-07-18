"""Two-stage issue retrieval: rank files, then rank AST chunks inside them.

The single-stage pipeline in :mod:`.retrieve_issue` ranks every chunk in the repository
and cuts the top-k. That makes the chunk budget do two jobs at once — pick the right
files *and* pick the right code inside them — and on a large repository the first job
eats the budget: fifteen chunks of elasticsearch cover only ~6 distinct files.

Here the jobs are split:

1. :func:`~gitflame_coderag.retrieval.file_level.file_search` keeps ``file_top_n`` files
   (optionally widened by symbol references, see ``expand_references``).
2. Only those files are chunked and embedded, and the ordinary BM25/dense/AST + RRF +
   reranker stack from :mod:`.retrieve_issue` ranks their chunks.

The output is still AST chunks — that is what the model consumes — but ``max_chunks_per_file``
stops one file from spending the whole evidence budget on overlapping class/method chunks
of the same code.

The practical consequence is that the repository is never chunked or embedded up front:
stage 2 works on the ~1.6k chunks of 100 candidate files, not on 361k.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from time import perf_counter

from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.chunking.ast_grep import extract_structural_metadata
from gitflame_coderag.pipelines.retrieve_issue import rank_issue_candidates
from gitflame_coderag.retrieval.dense import DenseIndex
from gitflame_coderag.retrieval.evidence import build_evidence_chunks
from gitflame_coderag.retrieval.file_level import (
    FileCandidate,
    FileIndex,
    expand_by_references,
    file_search,
)
from gitflame_coderag.retrieval.selection import ContextSelectionStats, select_context_results
from gitflame_coderag.schemas import (
    AIConfig,
    CodeChunk,
    EvidenceBuildResult,
    Issue,
    RepositoryFile,
    RetrievalResult,
    StructuralMetadata,
    TwoStageConfig,
)

DenseIndexBuilder = Callable[[list[CodeChunk], dict[str, StructuralMetadata]], DenseIndex]
"""Embeds candidate chunks on demand. Supplied by the caller so this module stays free of
model loading and caching concerns; ``None`` means dense retrieval is off."""


@dataclass(frozen=True)
class ChunkSet:
    """The chunks of one stage-1 candidate set, and what building them cost.

    ``build_seconds`` travels with the chunks because a caller may serve several configs of
    the same issue from one cached set: the honest chunking cost of each config is what the
    set cost to build, not what this particular call spent looking it up.
    """

    chunks: list[CodeChunk]
    metadata: dict[str, StructuralMetadata]
    build_seconds: float


ChunkBuilder = Callable[[list[RepositoryFile]], ChunkSet]
"""Chunks the stage-1 candidate files. Supplied by the caller so caching across the configs
of one issue lives outside this module; ``None`` means chunk them here, uncached."""


@dataclass
class TwoStageResult:
    evidence: EvidenceBuildResult
    stage1_candidates: list[FileCandidate]
    n_candidate_chunks: int
    context_selection: ContextSelectionStats
    timings: dict[str, float] = field(default_factory=dict)

    @property
    def candidate_paths(self) -> list[str]:
        return [candidate.path for candidate in self.stage1_candidates]


def run_two_stage_retrieval(
    issue: Issue,
    *,
    file_index: FileIndex,
    files_by_path: dict[str, RepositoryFile],
    ai_config: AIConfig,
    config: TwoStageConfig,
    query_text: str,
    query_vector: list[float] | None = None,
    chunk_builder: ChunkBuilder | None = None,
    dense_index_builder: DenseIndexBuilder | None = None,
    reranker_model: object | None = None,
) -> TwoStageResult:
    """Retrieve evidence chunks for ``issue`` in two stages.

    ``file_index`` must have been built with the same test-exclusion policy as
    ``config.exclude_tests``; it is reused across issues, so building it is the caller's job.

    Stage 1 reads nothing from ``config.stage2``, so every config of one issue that shares
    ``file_top_n`` and ``expand_references`` produces the same candidate files and the same
    chunks. Pass a caching ``chunk_builder`` to parse them once instead of once per config.
    """
    timings: dict[str, float] = {}

    started = perf_counter()
    seeds = file_search(query_text, file_index, config.file_top_n)
    candidates = seeds + expand_by_references(seeds, file_index, config.expand_references)
    timings["stage1_sec"] = perf_counter() - started

    if not candidates:
        return TwoStageResult(
            evidence=EvidenceBuildResult(evidence_chunks=[]),
            stage1_candidates=[],
            n_candidate_chunks=0,
            context_selection=ContextSelectionStats(
                candidate_count=0,
                selected_count=0,
                selected_file_count=0,
                selected_tokens=0,
            ),
            timings=timings,
        )

    candidate_files = [files_by_path[candidate.path] for candidate in candidates]
    chunk_set = (chunk_builder or _chunk_candidates(ai_config))(candidate_files)
    chunks, metadata = chunk_set.chunks, chunk_set.metadata
    timings["chunking_sec"] = chunk_set.build_seconds

    stage2 = config.stage2
    embeddings: DenseIndex | None = None
    if stage2.use_dense:
        if dense_index_builder is None or query_vector is None:
            raise ValueError(
                "Dense stage-2 retrieval requires both dense_index_builder and query_vector"
            )
        started = perf_counter()
        embeddings = dense_index_builder(chunks, metadata)
        timings["embedding_sec"] = perf_counter() - started

    started = perf_counter()
    # rank_issue_candidates builds the BM25 and AST indexes over the chunks it is given. That
    # is a per-issue cost here, but the candidate set is per-issue anyway, and ~1.6k chunks
    # index in milliseconds — the whole point of narrowing first.
    #
    # The ranked pool is deeper than final_top_k so the per-file cap has something to promote
    # into the slots it frees.
    pool_size = stage2.reranker_top_k if stage2.use_reranker else stage2.rrf_top_k
    ranked = rank_issue_candidates(
        issue=issue,
        chunks=chunks,
        metadata_by_chunk_id=metadata,
        config=stage2,
        embeddings=embeddings,
        query_vector=query_vector if stage2.use_dense else None,
        reranker_model=reranker_model if stage2.use_reranker else None,
        top_k=pool_size,
    )
    timings["stage2_sec"] = perf_counter() - started

    chunks_by_id = {chunk.id: chunk for chunk in chunks}
    selection = select_context_results(
        ranked,
        chunks_by_id,
        max_chunks=stage2.final_top_k,
        min_relevance_score=config.min_relevance_score,
        max_files=config.max_context_files,
        max_chunks_per_file=config.max_chunks_per_file,
        max_tokens=config.max_context_tokens,
        deduplicate_overlaps=config.deduplicate_overlaps,
        overlap_threshold=config.overlap_threshold,
    )

    return TwoStageResult(
        evidence=build_evidence_chunks(selection.results, chunks_by_id),
        stage1_candidates=candidates,
        n_candidate_chunks=len(chunks),
        timings=timings,
        context_selection=selection.stats,
    )


def _chunk_candidates(ai_config: AIConfig) -> ChunkBuilder:
    """The default, uncached :data:`ChunkBuilder`: parse the candidate files every call."""

    def build(files: list[RepositoryFile]) -> ChunkSet:
        started = perf_counter()
        chunks = build_chunks(files, ai_config)
        metadata = {chunk.id: extract_structural_metadata(chunk) for chunk in chunks}
        return ChunkSet(
            chunks=chunks,
            metadata=metadata,
            build_seconds=perf_counter() - started,
        )

    return build


def cap_chunks_per_file(
    results: list[RetrievalResult],
    chunks_by_id: dict[str, CodeChunk],
    *,
    cap: int,
) -> list[RetrievalResult]:
    """Drop a file's chunks past ``cap``, keeping rank order and re-numbering ranks.

    Ranking quality and evidence quality are not the same thing: the top of the list can be
    ten chunks of one file, all correct and all redundant, while the second file the issue
    touches never appears. Capping frees those slots for the next file down.
    """
    return select_context_results(
        results,
        chunks_by_id,
        max_chunks=len(results) or 1,
        max_chunks_per_file=cap,
    ).results
