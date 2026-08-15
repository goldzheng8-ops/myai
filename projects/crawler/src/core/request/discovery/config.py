from models.config.selector.base import SelectorConfig


from core.typing.config import BaseConfig
from core.request.discovery.typing import DiscoveryType
from core.request.profile import RequestProfile
from core.request.patch import RequestPatch

class DiscoveryConfig(BaseConfig):
    enabled: bool = True
    type: DiscoveryType


class ApiDiscoveryConfig(DiscoveryConfig):
    patch: RequestPatch
class UrlDiscoveryConfig(DiscoveryConfig):
    profile: RequestProfile


class HtmlDiscoveryConfig(UrlDiscoveryConfig):
    selector: SelectorConfig
class FeedDiscoveryConfig(UrlDiscoveryConfig):
    pass


class DetailLinkConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.DETAIL_LINK
class NextPageConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.NEXT_PAGE
class PageNumberConfig(HtmlDiscoveryConfig):
    type = DiscoveryType.PAGE_NUMBER


class RssConfig(FeedDiscoveryConfig):
    type = DiscoveryType.RSS
class SitemapConfig(FeedDiscoveryConfig):
    type = DiscoveryType.SITEMAP



class OffsetApiConfig(ApiDiscoveryConfig):
    parameter: str = "offset"
    limit: int = 20
    start: int = 0
class CursorApiConfig(ApiDiscoveryConfig):
    selector: SelectorConfig

class InfiniteScrollConfig(ApiDiscoveryConfig):
    selector: SelectorConfig
    scroll_count: int = 1
    scroll_delay: float = 0.5