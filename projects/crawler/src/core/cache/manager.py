from __future__ import annotations

from typing import Generic

from .plugin import CachePlugin
from .typing import K, V


class CacheManager(
    Generic[K, V],
):
    def __init__(self, cache: CachePlugin[K, V]) -> None:
        self._cache = cache

    @property
    def cache(self) -> CachePlugin[K, V]:
        return self._cache

    def get(self, key: K) -> V | None:
        return self._cache.get(key)

    def put(self, key: K, value: V) -> None:
        self._cache.put(key, value)

    def contains(self, key: K) -> bool:
        return self._cache.contains(key)

    def remove(self, key: K) -> None:
        self._cache.remove(key)

    def clear(self) -> None:
        self._cache.clear()

    def keys(self) -> tuple[K, ...]:
        return self._cache.keys()

    def size(self) -> int:
        return self._cache.size()