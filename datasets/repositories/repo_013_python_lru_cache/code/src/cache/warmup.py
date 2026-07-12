from __future__ import annotations
from typing import Callable, Iterable, Mapping


def warm_cache(cache, loader: Callable[[str], object], keys: Iterable[str]) -> int:
    """Pre-populate `cache` by loading each key through `loader`.

    Returns the number of keys successfully warmed.
    """
    warmed = 0
    for key in keys:
        value = loader(key)
        if value is not None:
            cache.put(key, value)
            warmed += 1
    return warmed


def warm_from_mapping(cache, source: Mapping[str, object]) -> int:
    """Pre-populate `cache` directly from an existing key/value mapping."""
    for key, value in source.items():
        cache.put(key, value)
    return len(source)
