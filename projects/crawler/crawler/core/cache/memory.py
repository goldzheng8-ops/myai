from __future__ import annotations

from core.cache.plugin import CachePlugin
from .typing import K, V


class MemoryCache(
    CachePlugin[K, V],
):
    type = "memory"

    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K, default: V | None = None) -> V | None:
        if key not in self._data:
            return default
        return self._data.get(key)

    def put(self, key: K, value: V) -> None:
        self._data[key] = value

    def contains(self, key: K) -> bool:
        return key in self._data

    def get_or_raise(self, key: K) -> V:
        if key not in self._data:
            raise KeyError(f"{key!r} not found in cache")
        return self._data[key]

    def put_if_absent(self, key: K, value: V) -> bool:
        if self.contains(key):
            return False
        self.put(key, value)
        return True

    def update(self, values: dict[K, V]) -> None:
        self._data.update(values)

    def remove(self, key: K) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> tuple[K, ...]:
        return tuple(self._data.keys())

    def size(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data