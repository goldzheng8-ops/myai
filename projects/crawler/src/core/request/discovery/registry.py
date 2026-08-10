
from typing import Any

from core.request.discovery.base import DiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from core.registry import Registry



class DiscoveryRegistry(
    Registry[
        DiscoveryType,
        DiscoveryPlugin[Any],
    ],
):
    pass