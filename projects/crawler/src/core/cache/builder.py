from __future__ import annotations

from typing import Any

from core.cache.registry import CacheRegistry
from core.cache.lru import LRUCache
from core.cache.memory import MemoryCache
from core.cache.ttl import TTLCache
from core.cache.weak import WeakCache
from core.cache.plugin import CachePlugin


class CacheBuilder:
    def __init__(self, registry: CacheRegistry | None = None) -> None:
        self._registry = registry or CacheRegistry()
        if not self._registry.contains("memory"):
            self._registry.register("memory", MemoryCache)
        if not self._registry.contains("lru"):
            self._registry.register("lru", LRUCache)
        if not self._registry.contains("ttl"):
            self._registry.register("ttl", TTLCache)
        if not self._registry.contains("weak"):
            self._registry.register("weak", WeakCache)

    def build(self, cache_type: str, **kwargs: Any) -> CachePlugin[Any, Any]:
        cache_cls = self._registry.get(cache_type)
        return cache_cls(**kwargs)

    def register(self, cache_type: str, cache_cls: type[CachePlugin[Any, Any]]) -> None:
        self._registry.register(cache_type, cache_cls)

    def contains(self, cache_type: str) -> bool:
        return self._registry.contains(cache_type)