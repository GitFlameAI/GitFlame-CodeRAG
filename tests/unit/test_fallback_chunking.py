from gitflame_coderag.chunking.fallback import chunk_file_fallback_window
from gitflame_coderag.schemas import AIConfig, FileMetadata, RepositoryFile


def test_fallback_chunking_preserves_original_line_numbers() -> None:
    content = "\n".join(f"line {number}" for number in range(1, 8))
    file = RepositoryFile(
        metadata=FileMetadata(
            id="repo:rev:sample.py",
            repository_id="repo",
            revision="rev",
            path="sample.py",
            extension=".py",
            language="python",
            size_bytes=len(content),
            line_count=7,
            content_hash="hash",
        ),
        raw_content=content,
    )
    config = AIConfig.model_validate(
        {"chunking": {"max_chunk_lines": 4, "overlap_lines": 1}}
    )

    chunks = chunk_file_fallback_window(file, config)

    assert [(chunk.start_line, chunk.end_line) for chunk in chunks] == [(1, 4), (4, 7)]

