from __future__ import annotations

from typing import Any

from core.provider.factory import FactoryProvider

class CachedProvider(
    FactoryProvider,
):

    def __init__(

        self,

        registry,

        manager,

        cache,

    ):

        self._cache = cache
    """
    Provider with cache management APIs.

    The default implementation behaves exactly like
    SingletonProvider.

    Future subclasses may implement:

    - TTL cache
    - LRU cache
    - Weak reference cache
    - Redis-backed cache
    """
    def get(self, service: type[Any]) -> Any:
        """
        Get a cached service instance.
        """
        return self._cache.get(service)

    def clear(self) -> None:
        """
        Clear all cached instances.
        """
        self._instances.clear()

    def invalidate(
        self,
        service: type[Any],
    ) -> None:
        """
        Remove a cached service instance.

        Does nothing if the service is not cached.
        """
        self._instances.pop(service, None)

