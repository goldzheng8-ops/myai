from config.discovery.base import DiscoveryConfig
from config.selector.base import SelectorConfig
from enums.discovery_type import DiscoveryType


class NextPageConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.NEXT_PAGE
    selector: SelectorConfig