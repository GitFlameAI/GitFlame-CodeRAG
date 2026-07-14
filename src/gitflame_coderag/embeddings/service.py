"""Embedding model adapter owned by the embeddings workstream."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

import numpy as np

from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ChunkKeywords,
    CodeChunk,
    StructuralMetadata,
)

DEFAULT_EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-base-code"
LIGHTWEIGHT_BASELINE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_STRING_RE = re.compile(
    r"""
    (?P<quote>['"])
    (?P<value>(?:\\.|(?! (?P=quote) ).)*)
    (?P=quote)
    """,
    re.VERBOSE | re.DOTALL,
)
_LINE_COMMENT_RE = re.compile(r"(?://|#)\s*(?P<comment>.*)")
_BLOCK_COMMENT_RE = re.compile(r"/\*(?P<comment>.*?)\*/", re.DOTALL)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")

_CODE_KEYWORDS = {
    "and",
    "as",
    "async",
    "await",
    "break",
    "case",
    "catch",
    "class",
    "const",
    "continue",
    "def",
    "default",
    "defer",
    "del",
    "do",
    "else",
    "enum",
    "except",
    "export",
    "extends",
    "false",
    "finally",
    "for",
    "from",
    "func",
    "function",
    "go",
    "if",
    "import",
    "in",
    "interface",
    "let",
    "match",
    "nil",
    "none",
    "not",
    "null",
    "or",
    "package",
    "pass",
    "private",
    "protected",
    "public",
    "raise",
    "return",
    "select",
    "self",
    "static",
    "struct",
    "switch",
    "this",
    "throw",
    "true",
    "try",
    "type",
    "var",
    "while",
    "with",
    "yield",
}

_COMMENT_STOPWORDS = _CODE_KEYWORDS | {
    "a",
    "an",
    "are",
    "be",
    "by",
    "can",
    "for",
    "from",
    "has",
    "have",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
}

_MODEL_CACHE: dict[str, object] = {}

# Peak GPU bytes reached by one batch of the most recent _encode_matrix call.
_LAST_ENCODE_PEAK_BYTES = 0

# Fraction of the GPU memory actually available to spend on one batch's attention.
# The rest absorbs fragmentation, the resident reranker, and whatever the desktop
# grabs mid-run. Exceeding real VRAM does not fail loudly on Windows -- the driver
# silently backs the allocation with system RAM and throughput collapses ~5x -- so
# the margin here is deliberately generous.
_ATTENTION_SAFETY_FRACTION = 0.6

# Starting guess for how many bytes one attention element (batch * heads * seq**2)
# costs. Measured at 2.9-7.5 bytes across batch/sequence shapes and SDPA backends,
# so this only has to be a safe upper bound for the very first batch: the real
# value is measured from that batch onwards and the estimate corrects itself.
_INITIAL_BYTES_PER_ELEMENT = 8.0

# Multiplier applied to the cost estimate when a batch OOMs anyway, so the retry
# is meaningfully smaller instead of failing again at nearly the same size.
_OOM_BACKOFF = 1.5

# Attention budget when there is no CUDA device to measure. CPU encoding is bounded
# by host RAM, which is both larger and not worth probing for.
_CPU_ATTENTION_BUDGET_BYTES = 512 * 1024**2

# Floor for the budget, so a nearly-full GPU still makes progress (one small batch
# at a time) instead of computing a budget that fits nothing.
_MIN_ATTENTION_BUDGET_BYTES = 64 * 1024**2

# How many batches make up one progress-reporting block in _encode_matrix.
_PROGRESS_BLOCK_BATCHES = 16

# Attention-matrix shape parameters, used only when they cannot be read off the
# loaded model. These match jina-embeddings-v2-base-code.
_FALLBACK_NUM_HEADS = 12
_FALLBACK_MAX_SEQ_LENGTH = 8192

# Texts per tokenizer call when measuring lengths; keeps peak list size bounded
# on repository-scale inputs.
_TOKENIZE_BLOCK_SIZE = 10_000

# Rough chars-per-token for code, used only when no tokenizer is available.
_CHARS_PER_TOKEN_ESTIMATE = 3


def build_embedding_text(chunk: CodeChunk, metadata: StructuralMetadata) -> str:
    header = [
        f"File: {chunk.path}",
        f"Language: {chunk.language}",
        f"Symbol: {chunk.symbol_name or ''}",
        f"Parent symbol: {chunk.parent_symbol or ''}",
        f"Node type: {chunk.node_type or ''}",
    ]
    if metadata.imports:
        header.append(f"Imports: {', '.join(metadata.imports)}")
    if metadata.calls:
        header.append(f"Calls: {', '.join(metadata.calls)}")
    if metadata.defined_symbols:
        header.append(f"Defined symbols: {', '.join(metadata.defined_symbols)}")
    if metadata.referenced_symbols:
        header.append(f"Referenced symbols: {', '.join(metadata.referenced_symbols)}")
    return "\n".join(header) + f"\n\nCode:\n{chunk.content}"


def extract_keywords_from_chunk(chunk: CodeChunk) -> ChunkKeywords:
    identifiers = _dedupe(
        identifier
        for identifier in [
            chunk.symbol_name,
            chunk.parent_symbol,
            *_IDENTIFIER_RE.findall(chunk.content),
        ]
        if identifier and identifier.lower() not in _CODE_KEYWORDS
    )
    identifier_tokens = _dedupe(
        token
        for identifier in identifiers
        for token in _split_identifier(identifier)
        if token not in _CODE_KEYWORDS
    )
    string_literals = _dedupe(
        _clean_literal(match.group("value")) for match in _STRING_RE.finditer(chunk.content)
    )
    comments_terms = _dedupe(
        token
        for comment in _extract_comments(chunk.content)
        for token in _WORD_RE.findall(comment.lower())
        if len(token) > 1 and token not in _COMMENT_STOPWORDS
    )
    path_tokens = _dedupe(
        token
        for part in re.split(r"[/.\-_]+", chunk.path)
        for token in _split_identifier(part)
        if token and token not in _CODE_KEYWORDS
    )

    return ChunkKeywords(
        chunk_id=chunk.id,
        identifiers=identifiers,
        identifier_tokens=identifier_tokens,
        string_literals=string_literals,
        comments_terms=comments_terms,
        path_tokens=path_tokens,
    )


def embed_text(
    text: str,
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
) -> list[float]:
    return _embed_texts(
        [text],
        model_name=model_name,
        batch_size=batch_size,
        normalize_vectors=normalize_vectors,
    )[0]


def embed_chunks(
    chunks: list[CodeChunk],
    metadata: dict[str, StructuralMetadata] | None = None,
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
) -> list[ChunkEmbedding]:
    if not chunks:
        return []

    metadata = metadata or {}
    texts = [
        build_embedding_text(chunk, metadata.get(chunk.id) or StructuralMetadata(chunk_id=chunk.id))
        for chunk in chunks
    ]
    vectors = _embed_texts(
        texts,
        model_name=model_name,
        batch_size=batch_size,
        normalize_vectors=normalize_vectors,
    )
    return [
        ChunkEmbedding(
            chunk_id=chunk.id,
            embedding_model=model_name,
            vector=vector,
        )
        for chunk, vector in zip(chunks, vectors, strict=True)
    ]


def embed_chunks_matrix(
    chunks: list[CodeChunk],
    metadata: dict[str, StructuralMetadata] | None = None,
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
    attention_budget_bytes: int | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> tuple[list[str], np.ndarray]:
    """Embed ``chunks`` into a ``(n, dim)`` float32 matrix, keeping vectors out of Python.

    Same embeddings as :func:`embed_chunks`, but the vectors never become
    ``list[float]``. That representation costs ~24 KB per 768-dim vector (~12 GB
    at 500k chunks) and is what makes repository-scale dense indexing infeasible;
    the matrix here is ~1.5 GB for the same input.

    ``batch_size`` is an upper bound: batches are sized to keep the attention matrix
    within ``attention_budget_bytes``, which defaults to a fraction of the GPU memory
    actually free at call time (see :func:`_encode_matrix`).
    ``progress_callback(done, total)`` is invoked periodically, so long runs can
    report how many chunks are finished and how many remain.
    """
    metadata = metadata or {}
    chunk_ids = [chunk.id for chunk in chunks]
    if not chunks:
        return chunk_ids, np.zeros((0, 0), dtype=np.float32)

    texts = [
        build_embedding_text(chunk, metadata.get(chunk.id) or StructuralMetadata(chunk_id=chunk.id))
        for chunk in chunks
    ]
    matrix = _encode_matrix(
        texts,
        model_name=model_name,
        batch_size=batch_size,
        normalize_vectors=normalize_vectors,
        attention_budget_bytes=attention_budget_bytes,
        progress_callback=progress_callback,
    )
    return chunk_ids, matrix


def embed_query(
    query: str,
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
) -> list[float]:
    return embed_text(
        query,
        model_name=model_name,
        batch_size=batch_size,
        normalize_vectors=normalize_vectors,
    )


def describe_embedding_backend(model_name: str = DEFAULT_EMBEDDING_MODEL) -> dict[str, str]:
    """Report the device and dtype the embedding model actually loaded onto."""
    model = _load_model(model_name)
    try:
        parameter = next(model.parameters())  # type: ignore[attr-defined]
        return {
            "model": model_name,
            "device": str(parameter.device),
            "dtype": str(parameter.dtype),
        }
    except Exception:  # noqa: BLE001 - reporting only, never fail a run over it
        return {"model": model_name, "device": "unknown", "dtype": "unknown"}


def _encode_matrix(
    texts: list[str],
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
    attention_budget_bytes: int | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> np.ndarray:
    """Encode ``texts`` into a float32 matrix, batching by measured attention cost.

    ``batch_size`` alone is the wrong knob for this model. jina-embeddings-v2 adds
    an ALiBi bias to the attention scores by summing it with the padding mask, and
    that sum broadcasts to a full ``(batch, heads, seq, seq)`` tensor. Peak memory
    therefore grows with ``batch * seq**2`` -- quadratically in the *longest text of
    the batch*. At ``batch_size=128`` a chunk of 1141 tokens already needs 3.7 GiB
    for that one tensor: enough to OOM an 8 GB card, and enough that longer chunks
    get silently backed by system RAM instead, collapsing throughput ~5x.

    So texts are sorted by token length and packed into batches that keep
    ``batch * heads * seq**2`` within the memory budget, with ``batch_size`` as an
    upper bound. Short chunks still ride full-size batches; only batches holding
    long chunks shrink, and only as far as they must.

    Both halves of that budget are measured rather than assumed, because guessing
    either one wrong is what silently wrecks throughput:

    * the budget itself comes from GPU memory actually free right now, so a resident
      reranker or a busy desktop shrinks it automatically;
    * the cost of one attention element is measured from the batches themselves --
      it ranges from ~3 to ~8 bytes depending on shape and SDPA backend, so no fixed
      constant is right for long.

    Vectors are returned in the caller's original order.
    """
    model = _load_model(model_name)
    total = len(texts)
    if total == 0:
        return np.zeros((0, 0), dtype=np.float32)

    lengths = _token_lengths(model, texts)
    # Longest first: the most expensive batch runs first, so a budget that cannot
    # fit this repository fails on batch one rather than an hour in.
    order = sorted(range(total), key=lambda index: lengths[index], reverse=True)
    heads = _num_attention_heads(model)
    cost = _AttentionCost()
    budget = attention_budget_bytes or _available_attention_budget()

    global _LAST_ENCODE_PEAK_BYTES
    _LAST_ENCODE_PEAK_BYTES = 0

    vectors_by_index: list[np.ndarray | None] = [None] * total
    cursor = 0
    done = 0
    batches_since_report = 0
    while cursor < total:
        batch = _next_batch(
            order,
            cursor,
            lengths,
            heads=heads,
            batch_size=batch_size,
            max_elements=cost.max_elements(budget),
        )
        try:
            encoded, peak_bytes = _encode_batch(
                model,
                [texts[index] for index in batch],
                normalize_vectors=normalize_vectors,
            )
        except RuntimeError as exc:
            if not _is_out_of_memory(exc) or len(batch) == 1:
                raise
            # The estimate was optimistic. Make it pessimistic enough that the retry
            # is meaningfully smaller, hand back the cached blocks, and re-pack the
            # same texts -- nothing is dropped, the batch just gets rebuilt smaller.
            cost.penalize()
            _release_cuda_cache()
            budget = attention_budget_bytes or _available_attention_budget()
            continue

        cost.observe(_attention_elements(batch, lengths, heads=heads), peak_bytes)
        _LAST_ENCODE_PEAK_BYTES = max(_LAST_ENCODE_PEAK_BYTES, peak_bytes)
        for index, vector in zip(batch, encoded, strict=True):
            vectors_by_index[index] = vector

        cursor += len(batch)
        done += len(batch)
        batches_since_report += 1
        if progress_callback is not None and (
            batches_since_report >= _PROGRESS_BLOCK_BATCHES or done == total
        ):
            progress_callback(done, total)
            batches_since_report = 0

    return np.asarray(vectors_by_index, dtype=np.float32)


@dataclass
class _AttentionCost:
    """Running estimate of the bytes one ``batch * heads * seq**2`` element costs.

    The estimate only ever grows. Encoding is a stream of differently shaped batches
    and an estimate that drifted down after a few cheap ones would hand the next
    expensive batch a budget it cannot honour, which on Windows does not fail --
    it spills to system RAM and quietly runs 5x slower.
    """

    bytes_per_element: float = _INITIAL_BYTES_PER_ELEMENT

    def max_elements(self, budget_bytes: int) -> int:
        return max(1, int(budget_bytes / self.bytes_per_element))

    def observe(self, elements: int, peak_bytes: int) -> None:
        if elements > 0 and peak_bytes > 0:
            self.bytes_per_element = max(self.bytes_per_element, peak_bytes / elements)

    def penalize(self) -> None:
        self.bytes_per_element *= _OOM_BACKOFF


def _next_batch(
    order: list[int],
    cursor: int,
    lengths: list[int],
    *,
    heads: int,
    batch_size: int,
    max_elements: int,
) -> list[int]:
    """Take the largest prefix of ``order[cursor:]`` that fits within ``max_elements``.

    ``order`` is sorted by length, so a batch is padded to a length close to its own
    longest text rather than to the longest text in the repository.
    """
    batch: list[int] = [order[cursor]]
    batch_max_length = lengths[order[cursor]]
    for index in order[cursor + 1 : cursor + batch_size]:
        candidate_max = max(batch_max_length, lengths[index])
        if (len(batch) + 1) * heads * candidate_max**2 > max_elements:
            break
        batch.append(index)
        batch_max_length = candidate_max
    return batch


def _attention_elements(batch: list[int], lengths: list[int], *, heads: int) -> int:
    """Attention elements a batch materializes: it pads to its longest member."""
    return len(batch) * heads * max(lengths[index] for index in batch) ** 2


def _encode_batch(
    model: object,
    texts: list[str],
    *,
    normalize_vectors: bool,
) -> tuple[np.ndarray, int]:
    """Encode one batch, returning the vectors and the GPU bytes it actually peaked at."""
    torch = _torch()
    measuring = torch is not None and torch.cuda.is_available()
    baseline = 0
    if measuring:
        torch.cuda.reset_peak_memory_stats()
        baseline = torch.cuda.memory_allocated()

    encoded = model.encode(  # type: ignore[attr-defined]
        texts,
        batch_size=len(texts),
        convert_to_numpy=True,
        normalize_embeddings=normalize_vectors,
        show_progress_bar=False,
    )

    peak_bytes = 0
    if measuring:
        peak_bytes = max(0, torch.cuda.max_memory_allocated() - baseline)
    return encoded, peak_bytes


def _available_attention_budget() -> int:
    """Bytes one batch's attention may occupy, from memory free on the device now.

    Only a fraction is spent: the rest absorbs fragmentation, the resident reranker,
    and the desktop. Blocks the caching allocator holds but is not using count as
    free, since PyTorch will reuse them before asking the driver for more.
    """
    torch = _torch()
    if torch is None or not torch.cuda.is_available():
        return _CPU_ATTENTION_BUDGET_BYTES

    free_bytes, _total = torch.cuda.mem_get_info()
    reusable = torch.cuda.memory_reserved() - torch.cuda.memory_allocated()
    usable = (free_bytes + max(0, reusable)) * _ATTENTION_SAFETY_FRACTION
    return max(_MIN_ATTENTION_BUDGET_BYTES, int(usable))


def last_encode_peak_bytes() -> int:
    """Peak GPU bytes a single batch of the last :func:`_encode_matrix` call reached.

    Lets a caller print what the encode actually cost instead of what it was
    budgeted, which is the number that shows whether the budget is sane.
    """
    return _LAST_ENCODE_PEAK_BYTES


def _num_attention_heads(model: object) -> int:
    try:
        return int(model[0].auto_model.config.num_attention_heads)  # type: ignore[index]
    except Exception:  # noqa: BLE001 - budgeting only, never fail a run over it
        return _FALLBACK_NUM_HEADS


def _is_out_of_memory(exc: BaseException) -> bool:
    """``torch.cuda.OutOfMemoryError`` subclasses ``RuntimeError``; so do driver OOMs."""
    return "out of memory" in str(exc).lower()


def _release_cuda_cache() -> None:
    torch = _torch()
    if torch is not None and torch.cuda.is_available():
        torch.cuda.empty_cache()


def _torch() -> Any:
    try:
        import torch
    except Exception:  # noqa: BLE001 - CPU-only or torch-less installs are fine
        return None
    return torch


def _token_lengths(model: object, texts: list[str]) -> list[int]:
    """Token length of each text, truncated to the model's max sequence length.

    Falls back to a character-based estimate when the model exposes no tokenizer
    (test stubs), which only affects how batches are packed, never the vectors.
    """
    max_seq_length = int(getattr(model, "max_seq_length", 0) or _FALLBACK_MAX_SEQ_LENGTH)
    tokenizer = getattr(model, "tokenizer", None)
    if tokenizer is None:
        return [
            min(max_seq_length, len(text) // _CHARS_PER_TOKEN_ESTIMATE + 1) for text in texts
        ]

    lengths: list[int] = []
    for start in range(0, len(texts), _TOKENIZE_BLOCK_SIZE):
        block = texts[start : start + _TOKENIZE_BLOCK_SIZE]
        encoded = tokenizer(
            block,
            add_special_tokens=True,
            truncation=True,
            max_length=max_seq_length,
            return_attention_mask=False,
            return_token_type_ids=False,
        )
        lengths.extend(len(ids) for ids in encoded["input_ids"])
    return lengths


def _embed_texts(
    texts: list[str],
    *,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
    normalize_vectors: bool = True,
) -> list[list[float]]:
    matrix = _encode_matrix(
        texts,
        model_name=model_name,
        batch_size=batch_size,
        normalize_vectors=normalize_vectors,
    )
    return [vector.astype(float).tolist() for vector in matrix]


def _load_model(model_name: str) -> object:
    cached_model = _MODEL_CACHE.get(model_name)
    if cached_model is not None:
        return cached_model

    import torch
    from sentence_transformers import SentenceTransformer

    # fp16 roughly halves latency on CUDA (see repo_large_001 benchmarking); CPU
    # kernels for fp16 are unreliable/unaccelerated, so stay on fp32 there.
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = SentenceTransformer(
        model_name,
        trust_remote_code=True,
        model_kwargs={"torch_dtype": dtype},
    )
    _enable_sdpa_attention(model)
    _MODEL_CACHE[model_name] = model
    return model


def _enable_sdpa_attention(model: object) -> None:
    """Switch jina's attention onto its ``scaled_dot_product_attention`` path.

    jina's remote modeling code ships both an SDPA path and an eager fallback, and
    picks between them on ``self.attn_implementation``. It reads that from its own
    config (which sets ``"torch"``), but transformers overwrites the attribute while
    loading, leaving it ``None`` -- so the eager path runs and materializes the
    ``(batch, heads, seq, seq)`` score matrix three times over (scores, scores+bias,
    softmax) instead of once. Measured on this repo's chunks: 1.4-2.3x the memory and
    1.3-1.5x the time, for identical vectors. Nothing here changes the math, so a
    model without that attribute is simply left alone.
    """
    for module in model.modules():  # type: ignore[attr-defined]
        if hasattr(module, "attn_implementation") and module.attn_implementation is None:
            module.attn_implementation = "torch"


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result


def _split_identifier(identifier: str) -> list[str]:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", identifier)
    normalized = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", normalized)
    raw_parts = re.split(r"[^A-Za-z0-9]+", normalized)
    return [
        part.lower()
        for part in raw_parts
        if part and not part.isdigit() and len(part) > 1
    ]


def _clean_literal(value: str) -> str:
    return " ".join(value.split())


def _extract_comments(content: str) -> list[str]:
    comments = [match.group("comment") for match in _BLOCK_COMMENT_RE.finditer(content)]
    comments.extend(match.group("comment") for match in _LINE_COMMENT_RE.finditer(content))
    return comments
