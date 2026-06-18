"""AST-Grep adapter owned by the AST/chunking workstream."""

from gitflame_coderag.schemas import AIConfig, CodeChunk, RepositoryFile, StructuralMetadata


def chunk_file_with_ast_grep(file: RepositoryFile, config: AIConfig) -> list[CodeChunk]:
    """Return AST-aware chunks for one file.

    Implement this adapter against the selected AST-Grep CLI or Python integration. Return an
    empty list when the language is unsupported or parsing fails, allowing fallback chunking.
    """
    raise NotImplementedError("AST-Grep integration is assigned to the chunking workstream")


def extract_structural_metadata(chunk: CodeChunk) -> StructuralMetadata:
    raise NotImplementedError("structural metadata extraction is not implemented yet")

