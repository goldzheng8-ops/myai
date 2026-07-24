from config.discovery.base import ApiDiscoveryConfig
from config.selector.base import SelectorConfig


class InfiniteScrollConfig(ApiDiscoveryConfig):

    selector: SelectorConfig

    scroll_count: int = 1

    scroll_delay: float = 0.5

