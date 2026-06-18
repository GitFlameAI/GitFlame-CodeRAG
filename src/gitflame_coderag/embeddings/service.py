"""Embedding model adapter owned by the embeddings workstream."""

from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ChunkKeywords,
    CodeChunk,
    StructuralMetadata,
)


def build_embedding_text(chunk: CodeChunk, metadata: StructuralMetadata) -> str:
    header = [
        f"File: {chunk.path}",
        f"Language: {chunk.language}",
        f"Symbol: {chunk.symbol_name or ''}",
        f"Node type: {chunk.node_type or ''}",
    ]
    if metadata.imports:
        header.append(f"Imports: {', '.join(metadata.imports)}")
    return "\n".join(header) + f"\n\nCode:\n{chunk.content}"


def extract_keywords_from_chunk(chunk: CodeChunk) -> ChunkKeywords:
    raise NotImplementedError


def embed_text(text: str) -> list[float]:
    raise NotImplementedError


def embed_chunks(chunks: list[CodeChunk]) -> list[ChunkEmbedding]:
    raise NotImplementedError


def embed_query(query: str) -> list[float]:
    return embed_text(query)

