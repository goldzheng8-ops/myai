
from typing import Any

from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.registry import Registry



class DiscoveryRegistry(
    Registry[
        DiscoveryType,
        DiscoveryPlugin[Any],
    ],
):
    pass