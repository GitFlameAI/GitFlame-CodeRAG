from gitflame_coderag.chunking.ast_grep import chunk_file_with_ast_grep
from gitflame_coderag.chunking.fallback import chunk_file_fallback_window
from gitflame_coderag.schemas import AIConfig, CodeChunk, RepositoryFile


def build_chunks(files: list[RepositoryFile], config: AIConfig) -> list[CodeChunk]:
    chunks: list[CodeChunk] = []
    for file in files:
        ast_chunks: list[CodeChunk] = []
        if config.chunking.strategy == "ast_aware":
            try:
                ast_chunks = chunk_file_with_ast_grep(file, config)
            except (NotImplementedError, RuntimeError):
                ast_chunks = []
        chunks.extend(ast_chunks or chunk_file_fallback_window(file, config))
    return chunks

