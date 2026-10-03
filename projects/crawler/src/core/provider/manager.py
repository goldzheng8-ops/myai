from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .protocol import ProviderResolver
from .registry import ProviderRegistry
from .typing import T

if TYPE_CHECKING:
    from .base import BaseProvider


class ProviderManager(
    ProviderResolver[Any, Any],
):

    def __init__(
        self,
        *,
        registry: ProviderRegistry,
        strategy_cls: type[BaseProvider],
    ) -> None:

        self._registry = registry
        self._default_strategy_cls = strategy_cls

        self._providers: dict[
            type[BaseProvider],
            BaseProvider,
        ] = {}

    @property
    def registry(
        self,
    ) -> ProviderRegistry:

        return self._registry

    def _get_provider(
        self,
        strategy_cls: type[BaseProvider],
    ) -> BaseProvider:

        provider = self._providers.get(strategy_cls)

        if provider is None:
            provider = strategy_cls(
                self._registry,
                self,
            )

            self._providers[strategy_cls] = provider

        return provider

    def resolve(
        self,
        key: type[T],
    ) -> T:

        registration = self._registry.get(key)

        strategy_cls = (
            registration.strategy_cls
            or self._default_strategy_cls
        )

        provider = self._get_provider(
            strategy_cls,
        )

        return provider.get(key)

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return self._registry.contains(service)

    def services(
        self,
    ) -> tuple[type[Any], ...]:

        return tuple(self._registry.keys())