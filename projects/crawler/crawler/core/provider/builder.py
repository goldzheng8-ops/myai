from typing import Any, Self

from core.provider.constructor_factory import ConstructorFactory
from core.provider.model import ProviderRegistration

from .factory import FactoryProvider
from .manager import ProviderManager
from .base import BaseProvider
from .registry import ProviderRegistry
from .typing import T, ProviderFactory


class ProviderBuilder:

    def __init__(
        self,
        *,
        strategy_cls: type[BaseProvider] = FactoryProvider,
    ) -> None:

        self._strategy_cls = strategy_cls
        self._registry = ProviderRegistry()

    def strategy(
        self,
        strategy_cls: type[BaseProvider],
    ) -> Self:

        self._strategy_cls = strategy_cls

        return self

    def _register(
        self,
        service: type[T],
        factory: ProviderFactory[T],
        *,
        strategy_cls: type[BaseProvider] | None = None,
    ) -> None:

        self._registry.register(
            service,
            ProviderRegistration(
                factory=factory,
                strategy_cls=strategy_cls,
            ),
        )

    def add_instance(
        self,
        service: type[T],
        instance: T,
        *,
        strategy_cls: type[BaseProvider] | None = None,
    ) -> Self:

        self._register(
            service,
            lambda _: instance,
            strategy_cls=strategy_cls,
        )

        return self

    def add_factory(
        self,
        service: type[T],
        factory: ProviderFactory[T],
        *,
        strategy_cls: type[BaseProvider] | None = None,
    ) -> Self:

        self._register(
            service,
            factory,
            strategy_cls=strategy_cls,
        )

        return self


    def add_type(
        self,
        service: type[T],
        implementation: type[T] | None = None,
        *,
        strategy_cls: type[BaseProvider] | None = None,
    ) -> Self:

        impl = implementation or service

        self._register(
            service,
            ConstructorFactory(impl),
            strategy_cls=strategy_cls,
        )

        return self

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return self._registry.contains(
            service,
        )

    def remove(
        self,
        service: type[Any],
    ) -> Self:

        self._registry.unregister(
            service,
        )

        return self

    def clear(
        self,
    ) -> Self:

        self._registry.clear()

        return self

    def clone(self) -> Self:

        builder = self.__class__(
            strategy_cls=self._strategy_cls,
        )

        builder._registry = self._registry.copy()

        return builder

    def build(
        self,
    ) -> ProviderManager:

        registry = (
            self._registry
            .copy()
            .freeze()
        )

        return ProviderManager(
            registry=registry,
            strategy_cls=self._strategy_cls,
        )