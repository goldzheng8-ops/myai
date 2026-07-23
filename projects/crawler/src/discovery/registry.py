from collections.abc import Iterable
from typing import Any

from discovery.base import DiscoveryPlugin
from enums.discovery_type import DiscoveryType



class DiscoveryRegistry:

    def __init__(self, plugins: Iterable[DiscoveryPlugin[Any]] = ()):

        self._plugins: dict[DiscoveryType, DiscoveryPlugin[Any]] = {}

        for plugin in plugins:
            self.register(plugin)

    def register(self, plugin: DiscoveryPlugin[Any]):

        if plugin.discovery_type in self._plugins:
            raise ValueError(f"{plugin.discovery_type} already registered")

        self._plugins[plugin.discovery_type] = plugin

    def get(self, type: DiscoveryType) -> DiscoveryPlugin[Any]:

        return self._plugins[type]