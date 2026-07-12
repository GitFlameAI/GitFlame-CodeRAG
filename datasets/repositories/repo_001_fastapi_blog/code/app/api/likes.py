"""Like/unlike support for posts (in-memory)."""

_LIKES: dict[int, set[str]] = {}


def like_post(post_id: int, username: str) -> int:
    likers = _LIKES.setdefault(post_id, set())
    likers.add(username)
    return len(likers)


def unlike_post(post_id: int, username: str) -> int:
    likers = _LIKES.get(post_id, set())
    likers.discard(username)
    return len(likers)


def like_count(post_id: int) -> int:
    return len(_LIKES.get(post_id, set()))
