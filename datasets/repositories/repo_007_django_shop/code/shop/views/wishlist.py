_WISHLISTS: dict[str, set[int]] = {}


def add_to_wishlist(user_id: str, product_id: int) -> dict:
    _WISHLISTS.setdefault(user_id, set()).add(product_id)
    return {"status": 200, "count": len(_WISHLISTS[user_id])}


def remove_from_wishlist(user_id: str, product_id: int) -> dict:
    _WISHLISTS.get(user_id, set()).discard(product_id)
    return {"status": 200}


def get_wishlist(user_id: str) -> list[int]:
    return sorted(_WISHLISTS.get(user_id, set()))
