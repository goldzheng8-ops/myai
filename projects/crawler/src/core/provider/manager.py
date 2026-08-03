from typing import Any

from .base import BaseProvider
from .registry import ProviderRegistry
from .typing import T


class ProviderManager:

    def __init__(
        self,
        *,
        registry: ProviderRegistry,
        provider_cls: type[BaseProvider],
    ) -> None:

        self._registry = registry

        self._provider = provider_cls(
            registry,
            self,
        )

    @property
    def registry(
        self,
    ) -> ProviderRegistry:

        return self._registry

    def get(
        self,
        service: type[T],
    ) -> T:

        return self._provider.get(service)

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return self._registry.contains(service)

    def services(
        self,
    ) -> tuple[type[Any], ...]:

        return self._registry.services()