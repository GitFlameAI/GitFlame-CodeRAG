"""Tagging support for posts (in-memory, standalone from the core post store)."""

_POST_TAGS: dict[int, set[str]] = {}


def add_tag(post_id: int, tag: str) -> list[str]:
    tags = _POST_TAGS.setdefault(post_id, set())
    tags.add(tag.strip().lower())
    return sorted(tags)


def remove_tag(post_id: int, tag: str) -> list[str]:
    tags = _POST_TAGS.get(post_id, set())
    tags.discard(tag.strip().lower())
    return sorted(tags)


def tags_for_post(post_id: int) -> list[str]:
    return sorted(_POST_TAGS.get(post_id, set()))
