from typing import  Iterable, TypeVar

from core.registry.base import BasePluginRegistry
from core.plugin.base import Plugin


K = TypeVar("K")
P = TypeVar("P", bound=Plugin)

class SingletonPluginRegistry(
    BasePluginRegistry[K, P],
):

    def __init__(
        self,
        plugins: Iterable[type[P]] = (),
    ) -> None:

        super().__init__(plugins)

        self._instances: dict[K, P] = {}

    def create(
        self,
        key: K,
        *args: object,
        **kwargs: object,
    ) -> P:

        plugin = self._instances.get(key)

        if plugin is None:

            plugin = self.get(key)()

            self._instances[key] = plugin

        return plugin