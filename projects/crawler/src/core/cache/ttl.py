from __future__ import annotations

import time

from core.cache.plugin import CachePlugin
from .typing import K, V


class TTLCache(
    CachePlugin[K, V],
):

    type = "ttl"

    def __init__(self, ttl: float = 60.0) -> None:
        if ttl <= 0:
            raise ValueError("ttl must be greater than 0")
        self._ttl = ttl
        self._data: dict[K, tuple[V, float]] = {}

    def _purge_expired(self) -> None:
        now = time.monotonic()
        expired = [key for key, (_, expires_at) in self._data.items() if expires_at <= now]
        for key in expired:
            del self._data[key]

    def get(self, key: K) -> V | None:
        self._purge_expired()
        if key not in self._data:
            return None
        value, _ = self._data[key]
        return value

    def put(self, key: K, value: V) -> None:
        self._data[key] = (value, time.monotonic() + self._ttl)

    def contains(self, key: K) -> bool:
        self._purge_expired()
        return key in self._data

    def remove(self, key: K) -> None:
        self._data.pop(key, None)

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> tuple[K, ...]:
        self._purge_expired()
        return tuple(self._data.keys())

    def size(self) -> int:
        self._purge_expired()
        return len(self._data)