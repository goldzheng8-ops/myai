from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic


from .registry import Registry

from .types import (
    K,
    P,
    Provider,
)


class PluginRegistry(
    Registry[K, type[P]],
    Generic[K, P],
    ABC,
):
    """
    Base registry for Plugin types.
    """

    def __init__(
        self,
        plugins: Iterable[type[P]] = (),
    ) -> None:

        super().__init__()

        self._providers: dict[K, Provider[P]] = {}

        for plugin in plugins:
            self.install(plugin)

    # ---------------------------------------------------------

    def install(
        self,
        plugin: type[P],
    ) -> None:

        self.register(
            self.resolve_key(plugin),
            plugin,
        )

    @staticmethod
    def resolve_key(
        plugin: type[P],
    ) -> K:

        return plugin.plugin_type

    # ---------------------------------------------------------

    def bind(
        self,
        plugin: type[P],
        provider: Provider[P],
    ) -> None:

        self._providers[
            self.resolve_key(plugin)
        ] = provider

    def unbind(
        self,
        key: K,
    ) -> None:

        self._providers.pop(
            key,
            None,
        )

    def has_provider(
        self,
        key: K,
    ) -> bool:

        return key in self._providers

    # ---------------------------------------------------------

    @abstractmethod
    def create(
        self,
        key: K,
    ) -> P:
        ...