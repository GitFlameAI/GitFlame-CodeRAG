"""Document-level chunking: one chunk per file, no AST parsing.

Whole-file chunks are the recall-maximizing representation: nothing in a file can
be lost between chunk boundaries. They are the stage-1 unit of the two-stage
pipeline, where the selected documents are afterwards split with AST-Grep.
"""

from __future__ import annotations

from hashlib import sha256

from gitflame_coderag.chunking.ast_grep import estimate_token_count, hash_chunk_content
from gitflame_coderag.schemas import CodeChunk, RepositoryFile


def build_document_chunks(files: list[RepositoryFile]) -> list[CodeChunk]:
    """Turn every non-empty repository file into exactly one document chunk."""

    documents: list[CodeChunk] = []
    for file in files:
        document = chunk_file_as_document(file)
        if document is not None:
            documents.append(document)
    return documents


def chunk_file_as_document(file: RepositoryFile) -> CodeChunk | None:
    """Return the whole file as a single ``chunk_type="file"`` chunk.

    Returns ``None`` for blank files, which carry no retrievable signal.
    """

    content = file.raw_content
    if not content.strip():
        return None

    line_count = max(1, len(content.splitlines()))
    return CodeChunk(
        id=make_document_chunk_id(file.metadata.id, file.metadata.content_hash),
        repository_id=file.metadata.repository_id,
        file_id=file.metadata.id,
        path=file.metadata.path,
        language=file.metadata.language,
        chunk_type="file",
        start_line=1,
        end_line=line_count,
        content=content,
        content_hash=hash_chunk_content(content),
        token_count=estimate_token_count(content),
    )


def make_document_chunk_id(file_id: str, content_hash: str) -> str:
    """Build a stable document chunk id from file identity and content."""

    digest = sha256(f"{file_id}|{content_hash}".encode()).hexdigest()[:16]
    return f"chunk_doc_{digest}"
