from models.enums.discovery_type import DiscoveryType
from models.config.discovery.base import HtmlDiscoveryConfig


class DetailLinkConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.DETAIL_LINK