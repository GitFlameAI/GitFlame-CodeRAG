from dataclasses import dataclass, field


@dataclass
class Review:
    product_id: int
    author: str
    rating: int
    comment: str = ""


_REVIEWS: dict[int, list[Review]] = {}


def add_review(product_id: int, author: str, rating: int, comment: str = "") -> dict:
    if not 1 <= rating <= 5:
        return {"status": 400, "error": "rating must be 1-5"}
    review = Review(product_id=product_id, author=author, rating=rating, comment=comment)
    _REVIEWS.setdefault(product_id, []).append(review)
    return {"status": 201}


def list_reviews(product_id: int) -> list[dict]:
    return [vars(r) for r in _REVIEWS.get(product_id, [])]
