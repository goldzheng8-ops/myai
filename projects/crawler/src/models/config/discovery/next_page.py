from models.enums.discovery_type import DiscoveryType
from models.config.discovery.base import HtmlDiscoveryConfig


class NextPageConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.NEXT_PAGE