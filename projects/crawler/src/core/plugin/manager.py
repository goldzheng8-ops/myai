from typing import Generic

from core.registry.base import Registry
from core.provider.protocol import BaseProvider
from core.plugin.typing import K, P
class PluginManager(
    Generic[K, P],
):

    def __init__(

        self,

        registry: Registry[K, type[P]],

        provider: BaseProvider,

    ):

        self._registry = registry
        self._provider = provider

    def create(
        self,
        key: K,
    ) -> P:

        plugin_cls = self._registry.get(key)

        return self._provider.get(
            plugin_cls,
        )