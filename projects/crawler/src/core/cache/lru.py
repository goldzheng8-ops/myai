from __future__ import annotations

from collections import OrderedDict

from core.cache.plugin import CachePlugin
from .typing import K, V


class LRUCache(
    CachePlugin[K, V],
):

    type = "lru"

    def __init__(self, maxsize: int = 512) -> None:
        if maxsize <= 0:
            raise ValueError("maxsize must be greater than 0")
        self._maxsize = maxsize
        self._data: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        value = self._data.pop(key)
        self._data[key] = value
        return value

    def put(self, key: K, value: V) -> None:
        if key in self._data:
            self._data.pop(key)
        self._data[key] = value
        if len(self._data) > self._maxsize:
            self._data.popitem(last=False)

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