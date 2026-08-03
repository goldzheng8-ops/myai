from collections.abc import Callable
from typing import Self

from .factory import FactoryProvider
from .manager import ProviderManager
from .base import BaseProvider
from .registry import ProviderRegistry
from .typing import T


class ProviderBuilder:

    def __init__(
        self,
        provider_cls: type[BaseProvider] = FactoryProvider,
    ) -> None:

        self._provider_cls = provider_cls
        self._registry = ProviderRegistry()

    def register(
        self,
        service: type[T],
        factory: Callable[[ProviderManager], T],
    ) -> Self:

        self._registry.register(
            service,
            factory,
        )

        return self

    def provider(
        self,
        provider_cls: type[BaseProvider],
    ) -> Self:

        self._provider_cls = provider_cls
        return self

    def clone(self) -> Self:

        builder = self.__class__(
            self._provider_cls,
        )

        builder._registry = self._registry.copy()

        return builder

    def build(
        self,
    ) -> ProviderManager:

        registry = self._registry.copy()

        registry.freeze()

        return ProviderManager(
            registry=registry,
            provider_cls=self._provider_cls,
        )