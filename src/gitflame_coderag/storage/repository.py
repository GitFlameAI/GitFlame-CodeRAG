"""Persistence interfaces owned by the storage workstream."""

from sqlalchemy import Engine

from gitflame_coderag.schemas import (
    ChunkEmbedding,
    ChunkKeywords,
    CodeChunk,
    FileMetadata,
    Repository,
    StructuralMetadata,
)


class CodeRAGRepository:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def save_repository(self, repository: Repository) -> None:
        raise NotImplementedError

    def save_file_metadata(self, metadata: FileMetadata) -> None:
        raise NotImplementedError

    def save_chunk(self, chunk: CodeChunk) -> None:
        raise NotImplementedError

    def save_structural_metadata(self, metadata: StructuralMetadata) -> None:
        raise NotImplementedError

    def save_bm25_text(self, chunk_id: str, text: str) -> None:
        raise NotImplementedError

    def save_embedding_text(self, chunk_id: str, text: str) -> None:
        raise NotImplementedError

    def save_embedding_vector(self, embedding: ChunkEmbedding) -> None:
        raise NotImplementedError

    def save_keywords(self, keywords: ChunkKeywords) -> None:
        raise NotImplementedError

    def load_chunks_for_repository(self, repository_id: str, revision: str) -> list[CodeChunk]:
        raise NotImplementedError

