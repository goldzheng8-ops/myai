from discovery.config.base import DiscoveryConfig
from discovery.config.enums import DiscoveryType

class InfiniteScrollConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.INFINITE_SCROLL
    max_scroll: int = 20
    wait: float = 1.5