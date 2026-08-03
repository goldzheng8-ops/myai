from .base import BaseProvider
from .typing import T
from .manager import ProviderManager
from .registry import ProviderRegistry


class FactoryProvider(
    BaseProvider,
):

    def __init__(
        self,
        registry: ProviderRegistry,
        manager: ProviderManager,
    ) -> None:

        self._registry = registry
        self._manager = manager

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

        factory = self._registry.factory(
            service,
        )

        return factory(
            self._manager,
        )

    def get(
        self,
        service: type[T],
    ) -> T:

        return self._create(
            service,
        )