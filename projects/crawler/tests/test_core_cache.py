import gc
import time

from core.cache.builder import CacheBuilder
from core.cache.lru import LRUCache
from core.cache.memory import MemoryCache
from core.cache.manager import CacheManager
from core.cache.ttl import TTLCache
from core.cache.weak import WeakCache


def test_memory_cache_round_trip() -> None:
    cache = MemoryCache[str, int]()
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.contains("a") is True
    assert cache.size() == 1
    assert tuple(cache.keys()) == ("a",)

    cache.remove("a")
    assert cache.contains("a") is False
    assert cache.size() == 0


def test_lru_cache_eviction() -> None:
    cache = LRUCache[str, int](maxsize=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)

    assert cache.contains("a") is False
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_ttl_cache_expiration() -> None:
    cache = TTLCache[str, int](ttl=0.05)
    cache.put("a", 1)
    assert cache.get("a") == 1
    time.sleep(0.1)
    assert cache.get("a") is None


def test_weak_cache_uses_weak_references() -> None:
    class Payload:
        pass

    payload = Payload()
    cache = WeakCache[str, Payload]()
    cache.put("p", payload)
    assert cache.contains("p") is True

    del payload
    gc.collect()
    assert cache.contains("p") is False


def test_cache_builder_and_manager() -> None:
    builder = CacheBuilder()
    memory = builder.build("memory")
    manager = CacheManager(memory)

    manager.put("x", 42)
    assert manager.get("x") == 42
    assert manager.size() == 1

    assert isinstance(builder.build("lru"), LRUCache)
    assert isinstance(builder.build("ttl"), TTLCache)
    assert isinstance(builder.build("weak"), WeakCache)
