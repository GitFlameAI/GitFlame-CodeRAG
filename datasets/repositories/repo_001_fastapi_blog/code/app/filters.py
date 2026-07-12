"""Small filtering helpers shared by list endpoints."""


def filter_by_author(posts: list[dict], author: str | None) -> list[dict]:
    """Return only posts written by the given author, or all posts if falsy."""
    if not author:
        return posts
    return [p for p in posts if p["author"] == author]


def filter_published(posts: list[dict], published_only: bool = False) -> list[dict]:
    """Return only published posts when requested."""
    if not published_only:
        return posts
    return [p for p in posts if p.get("published", True)]
