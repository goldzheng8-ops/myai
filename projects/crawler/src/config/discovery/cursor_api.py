

from config.discovery.base import DiscoveryConfig
from enums.discovery_type import DiscoveryType


class ApiCursorConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.CURSOR_API

    expression: str