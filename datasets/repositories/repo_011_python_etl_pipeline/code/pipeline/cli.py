from __future__ import annotations
import argparse
from pathlib import Path

from pipeline.config import PipelineConfig
from pipeline.runner import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the ETL pipeline")
    parser.add_argument("inputs", nargs="+", help="input CSV files")
    parser.add_argument("--output", default=PipelineConfig().output_path)
    args = parser.parse_args(argv)

    inputs = [Path(p) for p in args.inputs]
    count = run(inputs, Path(args.output))
    print(f"wrote {count} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
