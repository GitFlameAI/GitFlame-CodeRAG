from __future__ import annotations
from datetime import datetime

DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%m/%d/%Y",
    "%Y-%m-%dT%H:%M:%S",
)


def parse_date_multi(value: str) -> str:
    """Parse a date string trying several common formats, return ISO format."""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).isoformat()
        except ValueError:
            continue
    raise ValueError(f"unrecognized date format: {value!r}")
