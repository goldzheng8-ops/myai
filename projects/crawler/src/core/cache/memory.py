from __future__ import annotations

from core.cache.plugin import CachePlugin
from .typing import K, V


class MemoryCache(
    CachePlugin[K, V],
):
    type = "memory"

    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def put(self, key: K, value: V) -> None:
        self._data[key] = value

    def contains(self, key: K) -> bool:
        return key in self._data

    def remove(self, key: K) -> None:
        if key in self._data:
            del self._data[key]

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> tuple[K, ...]:
        return tuple(self._data.keys())

    def size(self) -> int:
        return len(self._data)