"""Simple keyword search across posts."""

from app.db import session


def search_posts(keyword: str) -> list[dict]:
    """Return posts whose title or body contains keyword (case-insensitive)."""
    if not keyword:
        return []
    needle = keyword.lower()
    with session() as db:
        return [
            p
            for p in db.posts.values()
            if needle in p["title"].lower() or needle in p["body"].lower()
        ]
