from discovery.config.base import DiscoveryConfig
from discovery.config.enums import DiscoveryType


class PageNumberConfig(DiscoveryConfig):
    type: DiscoveryType = DiscoveryType.PAGE_NUMBER
    page_param: str = "page"
    start_page: int
    max_pages: int


