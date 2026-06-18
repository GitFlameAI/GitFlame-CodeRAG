import hashlib

from gitflame_coderag.schemas import AIConfig, CodeChunk, RepositoryFile


def chunk_file_fallback_window(file: RepositoryFile, config: AIConfig) -> list[CodeChunk]:
    lines = file.raw_content.splitlines()
    if not lines:
        return []

    window = config.chunking.max_chunk_lines
    overlap = min(config.chunking.overlap_lines, window - 1)
    step = window - overlap
    chunks: list[CodeChunk] = []

    for offset in range(0, len(lines), step):
        chunk_lines = lines[offset : offset + window]
        if not chunk_lines:
            break
        start_line = offset + 1
        end_line = offset + len(chunk_lines)
        content = "\n".join(chunk_lines)
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        chunks.append(
            CodeChunk(
                id=f"{file.metadata.id}:{start_line}-{end_line}",
                repository_id=file.metadata.repository_id,
                file_id=file.metadata.id,
                path=file.metadata.path,
                language=file.metadata.language,
                chunk_type="fixed_window",
                start_line=start_line,
                end_line=end_line,
                content=content,
                content_hash=digest,
                token_count=len(content.split()),
            )
        )
        if end_line == len(lines):
            break
    return chunks

