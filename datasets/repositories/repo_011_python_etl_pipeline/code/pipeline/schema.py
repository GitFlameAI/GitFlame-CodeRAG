from __future__ import annotations

REQUIRED_FIELDS = ("id", "name", "amount", "created_at")


def validate_schema(row: dict, required: tuple[str, ...] = REQUIRED_FIELDS) -> list[str]:
    """Return the list of required fields missing from row."""
    return [field for field in required if field not in row]


def is_valid(row: dict, required: tuple[str, ...] = REQUIRED_FIELDS) -> bool:
    return not validate_schema(row, required)
