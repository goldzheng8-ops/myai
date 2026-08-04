from typing import Any

from core.cache.protocol import Cache
from core.provider.factory import FactoryProvider
from core.provider.manager import ProviderManager
from core.provider.registry import ProviderRegistry


class CachedProvider(
    FactoryProvider,
):

    def __init__(
        self,
        registry: ProviderRegistry,
        manager: ProviderManager,
        cache: Cache[type[Any], Any],
    ) -> None:
        super().__init__(registry, manager)
        self._cache = cache

    def get(self, service: type[Any]) -> Any:
        if self._cache.contains(service):
            return self._cache.get(service)

        instance = self._create(service)
        self._cache.put(service, instance)
        return instance

    def clear(self) -> None:
        self._cache.clear()

    def invalidate(self, service: type[Any]) -> None:
        self._cache.remove(service)