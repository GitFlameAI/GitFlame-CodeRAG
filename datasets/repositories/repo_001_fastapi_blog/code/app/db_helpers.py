"""Cross-entity helpers for cascading operations against the in-memory store."""

from app.db import session


def delete_comments_for_post(post_id: int) -> int:
    """Delete every comment attached to a post. Returns the number removed."""
    with session() as db:
        to_delete = [cid for cid, c in db.comments.items() if c["post_id"] == post_id]
        for cid in to_delete:
            del db.comments[cid]
        return len(to_delete)


def post_exists(post_id: int) -> bool:
    with session() as db:
        return post_id in db.posts
