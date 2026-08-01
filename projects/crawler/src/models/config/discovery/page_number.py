from models.enums.discovery_type import DiscoveryType
from models.config.discovery.base import HtmlDiscoveryConfig

class PageNumberConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.PAGE_NUMBER


