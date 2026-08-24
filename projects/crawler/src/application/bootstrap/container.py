from __future__ import annotations

from typing import Any, TypeVar

from core.provider import ProviderManager


T = TypeVar("T")


class ApplicationContainer:
    """
    Application-level dependency container.

    The container does not implement dependency injection itself.
    It delegates dependency resolution to the frozen core ProviderManager.

    Responsibilities:

    - expose application services
    - provide dependency resolution
    - own the application-level ProviderManager
    """

    def __init__(
        self,
        providers: ProviderManager,
    ) -> None:
        self._providers = providers

    @property
    def providers(self) -> ProviderManager:
        return self._providers

    def resolve(
        self,
        service: type[T],
    ) -> T:
        return self._providers.resolve(service)

    def contains(
        self,
        service: type[Any],
    ) -> bool:
        return self._providers.contains(service)