from typing import Annotated, Literal

from core.request.typing import RequestKind
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.transform.config import TransformConfigUnion
from core.typing.config import BaseConfig
from core.request.discovery.typing import DiscoveryType
from core.request.patch import RequestPatch
from pydantic import Field

class DiscoveryConfig(BaseConfig):
    target_spider:str
    request_kind: RequestKind
class UrlDiscoveryConfig(DiscoveryConfig):
    transforms: list[TransformConfigUnion] = Field(
        default_factory=list,
    )
class FeedDiscoveryConfig(UrlDiscoveryConfig):
    pass
class ApiDiscoveryConfig(DiscoveryConfig):
    patch: RequestPatch 


class HtmlDiscoveryConfig(UrlDiscoveryConfig):
    type: Literal[DiscoveryType.HTML] = DiscoveryType.HTML
    selector: SelectorConfigUnion
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

class PaginationDiscoveryConfig(
    UrlDiscoveryConfig,
):
    type: Literal[DiscoveryType.PAGINATION] = (
        DiscoveryType.PAGINATION
    )

    url_template: str

    start_page: int = 1
    end_page: int = 1
    step: int = 1

class FileDiscoveryConfig(UrlDiscoveryConfig):
    type: Literal[DiscoveryType.FILE] = DiscoveryType.FILE

    path: str
    encoding: str = "utf-8"
    strip: bool = True
    skip_empty: bool = True

DiscoveryConfigUnion = Annotated[
    (
        HtmlDiscoveryConfig
        | PaginationDiscoveryConfig
        | FileDiscoveryConfig
        | RssConfig
        | SitemapConfig
        | OffsetApiConfig
        | CursorApiConfig
        | InfiniteScrollConfig
    ),
    Field(discriminator="type"),
]