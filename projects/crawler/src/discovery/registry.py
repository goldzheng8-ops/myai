from collections.abc import Iterable

from discovery.base import DiscoveryPlugin
from discovery.config.enums import DiscoveryType


class DiscoveryRegistry:

    def __init__(self, plugins: Iterable[DiscoveryPlugin] = ()):

        self._plugins: dict[DiscoveryType, DiscoveryPlugin] = {}

        for plugin in plugins:
            self.register(plugin)

    def register(self, plugin: DiscoveryPlugin):

        if plugin.type in self._plugins:
            raise ValueError(f"{plugin.type} already registered")

        self._plugins[plugin.type] = plugin

    def get(self, type: DiscoveryType) -> DiscoveryPlugin:

        return self._plugins[type]