
from discovery.config.base import DiscoveryConfig
from discovery.config.enums import DiscoveryType


class ApiCursorConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.API_CURSOR

    expression: str