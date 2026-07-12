from gitflame_coderag.chunking.ast_grep import chunk_file_with_ast_grep, get_chunking_config
from gitflame_coderag.chunking.fallback import chunk_file_fallback_window
from gitflame_coderag.schemas import AIConfig, ChunkingConfig, CodeChunk, RepositoryFile


def build_chunks(files: list[RepositoryFile], config: AIConfig) -> list[CodeChunk]:
    chunks: list[CodeChunk] = []
    for file in files:
        chunks.extend(build_file_chunks(file, config))
    return chunks


def build_file_chunks(
    file: RepositoryFile,
    config: AIConfig | ChunkingConfig,
) -> list[CodeChunk]:
    """Chunk one file with AST-Grep, falling back to a fixed line window.

    Exposed separately from :func:`build_chunks` so the two-stage pipeline can
    split only the documents that stage 1 selected, instead of the whole repo.
    """
    chunking = get_chunking_config(config)
    ast_chunks: list[CodeChunk] = []
    if chunking.strategy == "ast_aware":
        try:
            ast_chunks = chunk_file_with_ast_grep(file, chunking)
        except (NotImplementedError, RuntimeError):
            ast_chunks = []
    return ast_chunks or chunk_file_fallback_window(file, chunking)
