"""Reusable pagination helper for list endpoints."""

from app.config import get_settings


def paginate(items: list, page: int = 1, page_size: int | None = None) -> list:
    """Return the slice of items for the given page.

    ``page`` is 1-indexed. ``page_size`` defaults to ``Settings.page_size``.
    """
    settings = get_settings()
    size = page_size or settings.page_size
    if page < 1:
        page = 1
    start = (page - 1) * size
    end = start + size
    return items[start:end]


def total_pages(total_items: int, page_size: int | None = None) -> int:
    settings = get_settings()
    size = page_size or settings.page_size
    if size <= 0:
        return 0
    return (total_items + size - 1) // size
