from enums.discovery_type import DiscoveryType
from config.discovery.base import HtmlDiscoveryConfig


class DetailLinkConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.DETAIL_LINK