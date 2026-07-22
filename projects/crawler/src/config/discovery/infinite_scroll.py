from config.discovery.base import DiscoveryConfig
from enums.discovery_type import DiscoveryType


class InfiniteScrollConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.INFINITE_SCROLL
    max_scroll: int = 20
    wait: float = 1.5