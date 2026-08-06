from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .protocol import Resolver
from .registry import ProviderRegistry
from .typing import T

if TYPE_CHECKING:
    from .base import BaseProvider


class ProviderManager(
    Resolver[Any,Any]
):

    def __init__(
        self,
        *,
        registry: ProviderRegistry,
        strategy_cls: type[BaseProvider],
    ) -> None:

        self._registry = registry

        self._strategy = strategy_cls(
            registry,
            self,
        )

    @property
    def registry(
        self,
    ) -> ProviderRegistry:

        return self._registry

    def resolve(
        self,
        key: type[T],
    ) -> T:

        return self._strategy.get(key)

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return self._registry.contains(service)

    def services(
        self,
    ) -> tuple[type[Any], ...]:

        return tuple(self._registry.keys())