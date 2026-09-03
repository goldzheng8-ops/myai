from typing import Annotated, Literal

from core.extraction.selector.config import SelectorConfigUnion
from core.typing.config import BaseConfig
from core.request.discovery.typing import DiscoveryType
from core.request.patch import RequestPatch
from pydantic import Field

class DiscoveryConfig(BaseConfig):
    pass
class UrlDiscoveryConfig(DiscoveryConfig):
    pass
class HtmlDiscoveryConfig(UrlDiscoveryConfig):
    selector: SelectorConfigUnion
class FeedDiscoveryConfig(UrlDiscoveryConfig):
    pass
class ApiDiscoveryConfig(DiscoveryConfig):
    patch: RequestPatch 


class DetailLinkConfig(HtmlDiscoveryConfig):
    type: Literal[DiscoveryType.DETAIL_LINK] = DiscoveryType.DETAIL_LINK
class NextPageConfig(HtmlDiscoveryConfig):
    type: Literal[DiscoveryType.NEXT_PAGE] = DiscoveryType.NEXT_PAGE
class PageNumberConfig(HtmlDiscoveryConfig):
    type: Literal[DiscoveryType.PAGE_NUMBER] = DiscoveryType.PAGE_NUMBER
class RssConfig(FeedDiscoveryConfig):
    type: Literal[DiscoveryType.RSS] = DiscoveryType.RSS
class SitemapConfig(FeedDiscoveryConfig):
    type: Literal[DiscoveryType.SITEMAP] = DiscoveryType.SITEMAP


class OffsetApiConfig(ApiDiscoveryConfig):
    type: Literal[DiscoveryType.OFFSET_API] = DiscoveryType.OFFSET_API
    parameter: str = "offset"
    limit: int = 20
    start: int = 0
class CursorApiConfig(ApiDiscoveryConfig):
    type: Literal[DiscoveryType.CURSOR_API] = DiscoveryType.CURSOR_API
    selector: SelectorConfigUnion
class InfiniteScrollConfig(ApiDiscoveryConfig):
    type: Literal[DiscoveryType.INFINITE_SCROLL] = (
        DiscoveryType.INFINITE_SCROLL
    )
    selector: SelectorConfigUnion
    scroll_count: int = 1
    scroll_delay: float = 0.5

DiscoveryConfigUnion = Annotated[
    (
        DetailLinkConfig
        | NextPageConfig
        | PageNumberConfig
        | RssConfig
        | SitemapConfig
        | OffsetApiConfig
        | CursorApiConfig
        | InfiniteScrollConfig
    ),
    Field(discriminator="type"),
]