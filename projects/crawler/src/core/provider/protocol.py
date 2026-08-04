from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any

from .typing import T

if TYPE_CHECKING:
    from .manager import ProviderManager
    from .registry import ProviderRegistry


class BaseProvider(
    ABC,
):

    def __init__(
        self,
        registry: ProviderRegistry,
        manager: ProviderManager,
    ) -> None:

        self._registry = registry
        self._manager = manager

    def get(
        self,
        service: type[T],
    ) -> T:

        raise NotImplementedError()

    def contains(
        self,
        service: type[Any],
    ) -> bool:

        return self._registry.contains(service)