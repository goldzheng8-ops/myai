from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .protocol import  Resolver
from .base import BaseProvider
from .typing import T

if TYPE_CHECKING:
    from .registry import ProviderRegistry


class FactoryProvider(
    BaseProvider,
):

    def __init__(
        self,
        registry: ProviderRegistry,
        resolver: Resolver[Any,Any],
    ) -> None:

        super().__init__(registry,resolver)

    def contains(
        self,
        service: type[T],
    ) -> bool:

        return self._registry.contains(
            service,
        )

    def _create(
        self,
        service: type[T],
    ) -> T:

        factory = self._registry.get(service)
        return factory(self._resolver)

    def get(
        self,
        service: type[T],
    ) -> T:

        return self._create(
            service,
        )