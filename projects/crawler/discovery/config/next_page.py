from discovery.config.base import DiscoveryConfig
from discovery.config.enums import DiscoveryType



class NextPageConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.NEXT_PAGE
    selector: SelectorConfig