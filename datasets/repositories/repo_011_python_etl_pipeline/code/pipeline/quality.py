from __future__ import annotations


def find_missing_fields(rows: list[dict], fields: list[str]) -> dict[int, list[str]]:
    """Return a mapping of row index -> list of missing fields."""
    problems: dict[int, list[str]] = {}
    for index, row in enumerate(rows):
        missing = [f for f in fields if f not in row or row[f] in (None, "")]
        if missing:
            problems[index] = missing
    return problems


def is_clean(rows: list[dict], fields: list[str]) -> bool:
    return not find_missing_fields(rows, fields)
