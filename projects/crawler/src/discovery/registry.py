
from typing import Any

from discovery.base import DiscoveryPlugin
from enums.discovery_type import DiscoveryType



from typing import Any

from registry.plugin_registry import PluginRegistry

class DiscoveryRegistry(
    PluginRegistry[
        DiscoveryType,
        DiscoveryPlugin[Any],
    ]
):

    pass