from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable

from .errors import (
    ProviderFrozenError,
    ServiceNotRegisteredError,
)
from .typing import (
    ProviderFactories,
    ProviderFactory,
    T,
)


class ProviderRegistry:
    """
    Registry of service factories.

    Responsible only for maintaining the mapping:

        Service -> Factory

    It never creates service instances.
    """

    def __init__(self) -> None:

        self._factories: ProviderFactories = {}
        self._frozen = False

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        self._frozen = True

    def register(
        self,
        service: type[T],
        factory: ProviderFactory[T],
    ) -> None:
        """
        Register a factory for a service.
        """

        if self._frozen:
            raise ProviderFrozenError(
                "ProviderRegistry is frozen."
            )

        self._factories[service] = factory

    def unregister(
        self,
        service: type[Any],
    ) -> None:
        """
        Remove a registered service.
        """

        if self._frozen:
            raise ProviderFrozenError(
                "ProviderRegistry is frozen."
            )

        self._factories.pop(service, None)

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return service in self._factories

    def factory(
        self,
        service: type[T],
    ) -> ProviderFactory[T]:
        """
        Get the factory of a service.
        """

        factory = self._factories.get(service)

        if factory is None:
            raise ServiceNotRegisteredError(
                f"Service not registered: {service!r}"
            )

        return factory

    def services(
        self,
    ) -> tuple[type[Any], ...]:
        """
        Return all registered services.
        """

        return tuple(self._factories.keys())

    def clear(self) -> None:
        """
        Remove all registrations.
        """

        if self._frozen:
            raise ProviderFrozenError(
                "ProviderRegistry is frozen."
            )

        self._factories.clear()

    def copy(self) -> ProviderRegistry:
        """
        Create a mutable copy.

        The copied registry is NOT frozen.
        """

        registry = ProviderRegistry()

        registry._factories = deepcopy(
            self._factories,
        )

        return registry

    def __contains__(
        self,
        service: type[Any],
    ) -> bool:

        return self.contains(service)

    def __len__(
        self,
    ) -> int:

        return len(self._factories)

    def __iter__(
        self,
    )-> Iterable[tuple[type[Any], ProviderFactory[Any]]]:

        return iter(
            self._factories.items(),
        )