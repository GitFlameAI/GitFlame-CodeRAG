from __future__ import annotations


def keep_first(rows: list[dict], key: str = "id") -> list[dict]:
    seen: set = set()
    unique = []
    for row in rows:
        if row[key] in seen:
            continue
        seen.add(row[key])
        unique.append(row)
    return unique


def keep_most_recent(rows: list[dict], key: str = "id", recency_field: str = "created_at") -> list[dict]:
    """Keep the most recent row per key, based on recency_field."""
    latest: dict = {}
    for row in rows:
        current = latest.get(row[key])
        if current is None or row[recency_field] > current[recency_field]:
            latest[row[key]] = row
    return list(latest.values())
