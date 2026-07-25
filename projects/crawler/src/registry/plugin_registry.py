from __future__ import annotations

from abc import ABC
from typing import Generic, Iterable, TypeVar

from registry.plugin_base import Plugin

K = TypeVar("K")
P = TypeVar("P",bound=Plugin)


class PluginRegistry(
    Generic[K, P],
    ABC,
):
    """
    Generic plugin registry.

    Register plugin classes while lazily creating
    singleton plugin instances.
    """

    def __init__(
        self,
        plugins: Iterable[type[P]] = (),
    ) -> None:

        self._types: dict[K, type[P]] = {}

        self._instances: dict[K, P] = {}

        for plugin in plugins:
            self.register(plugin)

    def register(
        self,
        plugin: type[P],
    ) -> None:

        key = self.key(plugin)

        if key in self._types:
            raise ValueError(
                f"{key!r} already registered."
            )

        self._types[key] = plugin

    def get_type(
        self,
        key: K,
    ) -> type[P]:

        return self._types[key]

    def create(
        self,
        key: K,
    ) -> P:

        plugin = self._instances.get(key)

        if plugin is None:

            plugin_cls = self.get_type(key)

            plugin = plugin_cls()

            self._instances[key] = plugin

        return plugin

    @staticmethod
    def key(
        plugin: type[P],
    ) -> K:
        return plugin.plugin_type