from enums.discovery_type import DiscoveryType
from config.discovery.base import HtmlDiscoveryConfig


class NextPageConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.NEXT_PAGE