
from typing import Any

from discovery.base import DiscoveryPlugin
from enums.discovery_type import DiscoveryType
from core.registry.single import SingletonPluginRegistry



class DiscoveryRegistry(
    SingletonPluginRegistry[
        DiscoveryType,
        DiscoveryPlugin[Any],
    ],
):
    pass