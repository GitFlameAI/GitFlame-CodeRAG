from pathlib import Path
from typing import Any

import yaml

from gitflame_coderag.schemas import AIConfig


def load_ai_config(config_path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("repository config must contain a YAML mapping")
    return raw


def parse_ai_config(raw_config: dict[str, Any]) -> AIConfig:
    analysis = raw_config.get("analysis", {})
    return AIConfig.model_validate(
        {
            "version": raw_config.get("version", 1),
            "include": analysis.get("include", ["**/*"]),
            "exclude": analysis.get("exclude", []),
            "chunking": raw_config.get("chunking", {}),
            "retrieval": raw_config.get("retrieval", {}),
            "embeddings": raw_config.get("embeddings", {}),
        }
    )

