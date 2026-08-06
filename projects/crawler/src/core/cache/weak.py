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

    def get(self, key: K, default: V | None = None) -> V | None:
        if key not in self._data:
            return default
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        self._data[key] = value

    def contains(self, key: K) -> bool:
        return key in self._data

    def get_or_raise(self, key: K) -> V:
        if not self.contains(key):
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