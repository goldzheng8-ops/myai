from config.discovery.base import DiscoveryConfig
from enums.discovery_type import DiscoveryType

class PageNumberConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.PAGE_NUMBER
    page_param: str = "page"
    start_page: int
    max_pages: int


