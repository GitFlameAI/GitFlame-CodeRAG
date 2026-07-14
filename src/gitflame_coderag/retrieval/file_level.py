"""Stage-1 retrieval: narrow a repository to the handful of files worth chunking.

Chunk-level retrieval over a large repository spends its ranking budget badly. The
top-k it returns is a budget of *chunks*, but the thing an issue points at is a
*file*, and a single file can easily take ten of the fifteen slots with overlapping
class/method chunks. On elasticsearch (22.9k files, 361k chunks) fifteen chunks cover
only ~6 distinct files, which caps file recall long before the ranker's quality does.

This module ranks whole files instead, so the two budgets are decoupled: stage 1 keeps
N files, stage 2 spends its chunk budget only inside them. That also removes the need to
chunk and embed the entire repository up front — only the N candidates are.

Two signals:

``file_search``
    BM25Plus over the whole file text, with the path and the file's own name boosted.
    Same tokenizer and hyper-parameters as chunk-level BM25 (:mod:`.bm25`), so the two
    stages agree on what a term is.

``expand_by_references``
    A file that names another file's symbol is one hop from it. Issues describe symptoms
    ("bulk rejections return 500 instead of 429"), not mechanisms, so the file holding the
    mechanism can be lexically invisible while the file that *calls* it ranks high. On
    elasticsearch this is the difference between finding ``EsThreadPoolExecutor`` (BM25
    rank 98) and not: ``TransportBulkAction`` ranks 11th and references it by name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np

from gitflame_coderag.retrieval.bm25 import BM25_B, BM25_K1, tokenize_for_bm25
from gitflame_coderag.schemas import RepositoryFile

# BM25Plus's lower-bound term-frequency shift, matching rank_bm25's default.
BM25_DELTA = 1.0

# The file's own name is the strongest single signal that an issue is about it, and it is
# diluted to nothing inside a 2000-line file. Repeat it, as build_bm25_text does per chunk.
_PATH_WEIGHT = 3

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# A stem is only a usable symbol when it names one file: "module-info", "__init__", "index"
# and friends are owned by hundreds of files and would wire the whole repository together.
_MAX_STEM_OWNERS = 3
_MIN_STEM_LENGTH = 4


@dataclass(frozen=True)
class FileCandidate:
    """One stage-1 file, ranked."""

    path: str
    position: int
    rank: int
    score: float
    source: str  # "bm25" | "reference"


@dataclass
class FileIndex:
    """BM25 postings plus a symbol-reference graph over whole files.

    ``postings[term]`` is ``(file positions, BM25 weight of the term in that file)``, so a
    query only touches the files containing its terms — the same inverted layout
    :class:`~gitflame_coderag.retrieval.ast.AstIndex` uses, and the reason a query costs
    milliseconds where ``rank_bm25`` over 361k chunks costs ~4.5s.
    """

    paths: list[str]
    postings: dict[str, tuple[np.ndarray, np.ndarray]]
    references: list[np.ndarray]
    position_by_path: dict[str, int]

    def __len__(self) -> int:
        return len(self.paths)


def build_file_bm25_text(file: RepositoryFile) -> str:
    """Lexical representation of a whole file: boosted path and name, then raw content."""
    path = file.metadata.path
    basename = path.rsplit("/", 1)[-1]
    stem = basename.rsplit(".", 1)[0]
    parts = [path, *([basename] * _PATH_WEIGHT), *([stem] * _PATH_WEIGHT), file.raw_content]
    return "\n".join(part for part in parts if part)


def build_file_index(
    files: list[RepositoryFile],
    *,
    build_reference_graph: bool = True,
) -> FileIndex:
    """Index ``files`` for stage-1 retrieval.

    ``build_reference_graph=False`` skips the identifier scan when only BM25 is needed.
    """
    paths = [file.metadata.path for file in files]
    n_files = len(files)
    if n_files == 0:
        return FileIndex(paths=[], postings={}, references=[], position_by_path={})

    vocabulary: dict[str, int] = {}
    term_ids: list[int] = []
    term_frequencies: list[float] = []
    document_lengths = np.zeros(n_files, dtype=np.float32)
    entries_per_file = np.zeros(n_files, dtype=np.int64)
    identifiers_per_file: list[set[str]] = []

    for position, file in enumerate(files):
        counts: dict[str, float] = {}
        for token in tokenize_for_bm25(build_file_bm25_text(file)):
            counts[token] = counts.get(token, 0.0) + 1.0
        document_lengths[position] = sum(counts.values())
        entries_per_file[position] = len(counts)
        for term, frequency in counts.items():
            term_ids.append(vocabulary.setdefault(term, len(vocabulary)))
            term_frequencies.append(frequency)
        if build_reference_graph:
            identifiers_per_file.append(set(_IDENTIFIER_RE.findall(file.raw_content)))

    postings = _build_postings(
        term_ids=np.asarray(term_ids, dtype=np.int32),
        term_frequencies=np.asarray(term_frequencies, dtype=np.float32),
        entries_per_file=entries_per_file,
        document_lengths=document_lengths,
        vocabulary=vocabulary,
    )
    references = (
        _build_reference_graph(paths, identifiers_per_file)
        if build_reference_graph
        else [np.empty(0, dtype=np.int32) for _ in paths]
    )
    return FileIndex(
        paths=paths,
        postings=postings,
        references=references,
        position_by_path={path: position for position, path in enumerate(paths)},
    )


def file_search(query: str, index: FileIndex, top_k: int) -> list[FileCandidate]:
    """Rank files by BM25Plus against the issue query."""
    if top_k <= 0 or not index.paths:
        return []

    query_terms = tokenize_for_bm25(query)
    if not query_terms:
        return []

    scores = np.zeros(len(index.paths), dtype=np.float32)
    matched_any = False
    for term in query_terms:
        posting = index.postings.get(term)
        if posting is None:
            continue
        positions, weights = posting
        scores[positions] += weights
        matched_any = True
    if not matched_any:
        return []

    matched = np.flatnonzero(scores > 0)
    order = matched[np.lexsort((np.asarray(index.paths)[matched], -scores[matched]))]
    return [
        FileCandidate(
            path=index.paths[position],
            position=int(position),
            rank=rank,
            score=float(scores[position]),
            source="bm25",
        )
        for rank, position in enumerate(order[:top_k], start=1)
    ]


def expand_by_references(
    seeds: list[FileCandidate],
    index: FileIndex,
    limit: int,
) -> list[FileCandidate]:
    """Pull in files that the seeds name but BM25 could not see.

    A neighbour is scored by ``sum(1 / seed_rank)`` over the seeds referencing it, so being
    named by the top hit counts for more than being named by the fiftieth. Ranks continue
    from the seed list; the caller concatenates the two.
    """
    if limit <= 0 or not seeds:
        return []

    seed_positions = {seed.position for seed in seeds}
    scores: dict[int, float] = {}
    for seed in seeds:
        for neighbour in index.references[seed.position].tolist():
            if neighbour in seed_positions:
                continue
            scores[neighbour] = scores.get(neighbour, 0.0) + 1.0 / seed.rank

    ordered = sorted(scores.items(), key=lambda item: (-item[1], index.paths[item[0]]))[:limit]
    first_rank = len(seeds) + 1
    return [
        FileCandidate(
            path=index.paths[position],
            position=position,
            rank=first_rank + offset,
            score=score,
            source="reference",
        )
        for offset, (position, score) in enumerate(ordered)
    ]


def _build_postings(
    *,
    term_ids: np.ndarray,
    term_frequencies: np.ndarray,
    entries_per_file: np.ndarray,
    document_lengths: np.ndarray,
    vocabulary: dict[str, int],
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Turn flat (file, term, tf) entries into per-term postings of BM25Plus weights."""
    n_files = len(document_lengths)
    n_terms = len(vocabulary)
    file_of_entry = np.repeat(np.arange(n_files, dtype=np.int32), entries_per_file)

    # Each entry is one (file, term) pair, so counting entries per term counts documents.
    document_frequencies = np.bincount(term_ids, minlength=n_terms).astype(np.float32)
    inverse_document_frequency = np.log((n_files + 1) / document_frequencies).astype(np.float32)

    average_length = float(document_lengths.mean()) or 1.0
    length_norm = BM25_K1 * (1 - BM25_B + BM25_B * document_lengths / average_length)
    saturated = term_frequencies * (BM25_K1 + 1) / (term_frequencies + length_norm[file_of_entry])
    weights = inverse_document_frequency[term_ids] * (saturated + BM25_DELTA)

    order = np.argsort(term_ids, kind="stable")
    sorted_files = file_of_entry[order]
    sorted_weights = weights[order].astype(np.float32)
    bounds = np.concatenate(([0], np.cumsum(document_frequencies.astype(np.int64))))
    return {
        term: (
            sorted_files[bounds[term_id] : bounds[term_id + 1]],
            sorted_weights[bounds[term_id] : bounds[term_id + 1]],
        )
        for term, term_id in vocabulary.items()
    }


def _build_reference_graph(
    paths: list[str],
    identifiers_per_file: list[set[str]],
) -> list[np.ndarray]:
    """Link each file to the files whose symbol name it mentions."""
    owners: dict[str, list[int]] = {}
    for position, path in enumerate(paths):
        stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if len(stem) >= _MIN_STEM_LENGTH:
            owners.setdefault(stem, []).append(position)
    unambiguous = {
        stem: positions
        for stem, positions in owners.items()
        if len(positions) <= _MAX_STEM_OWNERS
    }

    references: list[np.ndarray] = []
    for position, identifiers in enumerate(identifiers_per_file):
        neighbours = {
            owner
            for identifier in identifiers & unambiguous.keys()
            for owner in unambiguous[identifier]
            if owner != position
        }
        references.append(np.asarray(sorted(neighbours), dtype=np.int32))
    return references
