from __future__ import annotations

from weakref import WeakValueDictionary

from core.cache.plugin import CachePlugin
from .typing import K, V


class WeakCache(
    CachePlugin[K, V],
):

    type = "weak"

    def __init__(self) -> None:
        self._data: WeakValueDictionary[K, V] = WeakValueDictionary()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        self._data[key] = value

    def contains(self, key: K) -> bool:
        return key in self._data

    def remove(self, key: K) -> None:
        self._data.pop(key, None)

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> tuple[K, ...]:
        return tuple(self._data.keys())

    def size(self) -> int:
        return len(self._data)