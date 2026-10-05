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

    def get(self, key: K, default: V | None = None) -> V | None:
        if key not in self._data:
            return default
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

    def get_or_raise(self, key: K) -> V:
        if not self.contains(key):
            raise KeyError(f"{key!r} not found in cache")
        value = self.get(key)
        assert value is not None
        return value

    def put_if_absent(self, key: K, value: V) -> bool:
        if self.contains(key):
            return False
        self.put(key, value)
        return True

    def update(self, values: dict[K, V]) -> None:
        for key, value in values.items():
            self.put(key, value)

    def remove(self, key: K) -> bool:
        if key in self._data:
            self._data.pop(key, None)
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