from typing import  TypeVar

from core.registry.base import BasePluginRegistry
from core.plugin.base import Plugin


K = TypeVar("K")
P = TypeVar("P", bound=Plugin)

class FactoryPluginRegistry(
    BasePluginRegistry[K, P],
):

    def create(
        self,
        key: K,
        *args: object,
        **kwargs: object,
    ) -> P:

        plugin_cls = self.get(key)

        return plugin_cls(
            *args,
            **kwargs,
        )