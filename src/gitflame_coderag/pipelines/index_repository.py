from pathlib import Path

from gitflame_coderag.chunking import build_chunks
from gitflame_coderag.config import load_ai_config, parse_ai_config
from gitflame_coderag.ingestion import filter_files_by_config, load_repository_files
from gitflame_coderag.schemas import CodeChunk


def index_repository(
    repo_path: Path,
    config_path: Path,
    repository_id: str,
    revision: str,
) -> list[CodeChunk]:
    """Run the in-memory Sprint 1 indexing flow.

    Persistence and search-representation creation are connected after their workstreams implement
    the storage, BM25, and embedding adapters.
    """
    config = parse_ai_config(load_ai_config(config_path))
    files = load_repository_files(repo_path, repository_id, revision)
    selected_files = filter_files_by_config(files, config)
    return build_chunks(selected_files, config)

