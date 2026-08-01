from typing import Generic
from .plugin import PluginRegistry


from .typing import (
    K,
    P,
)


class FactoryPluginRegistry(
    PluginRegistry[K, P],
    Generic[K, P],
):
    """
    Creates a new instance every time.
    """

    def create(
        self,
        key: K,
    ) -> P:

        provider = self._providers.get(key)

        if provider is not None:
            return provider()

        plugin_cls = self.get(key)

        return plugin_cls()