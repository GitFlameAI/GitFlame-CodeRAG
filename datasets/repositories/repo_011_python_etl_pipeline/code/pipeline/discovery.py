from __future__ import annotations
from pathlib import Path

from pipeline.config import PipelineConfig


def discover_inputs(config: PipelineConfig, base: Path = Path(".")) -> list[Path]:
    """Resolve config.input_glob to a sorted list of matching paths."""
    return sorted(base.glob(config.input_glob))
