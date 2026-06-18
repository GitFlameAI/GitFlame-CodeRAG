import argparse
from pathlib import Path

from gitflame_coderag.pipelines.index_repository import index_repository


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CodeRAG chunks for a repository")
    parser.add_argument("repo_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--revision", default="local")
    args = parser.parse_args()

    chunks = index_repository(
        args.repo_path,
        args.config_path,
        args.repository_id,
        args.revision,
    )
    print(f"Created {len(chunks)} chunks")


if __name__ == "__main__":
    main()

