from collections.abc import Callable
from typing import Any, TypeAlias

from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.plugins.cursor_api import CursorApiDiscovery
from core.request.discovery.plugins.detail_link import DetailLinkDiscovery
from core.request.discovery.plugins.infinite_scroll import InfiniteScrollDiscovery
from core.request.discovery.plugins.next_page import NextPageDiscovery
from core.request.discovery.plugins.offset_api import OffsetApiDiscovery
from core.request.discovery.plugins.page_number import PageNumberDiscovery
from core.request.discovery.plugins.rss import RssDiscovery
from core.request.discovery.plugins.sitemap import SitemapDiscovery

DiscoveryFactory: TypeAlias = Callable[
    [],
    DiscoveryPlugin[Any],
]

def create_cursor_api_discovery() -> CursorApiDiscovery:
    return CursorApiDiscovery()

def create_detail_link_discovery() -> DetailLinkDiscovery:
    return DetailLinkDiscovery()

def create_infinite_scroll_discovery() -> InfiniteScrollDiscovery:
    return InfiniteScrollDiscovery()

def create_next_page_discovery() -> NextPageDiscovery:
    return NextPageDiscovery()

def create_offset_api_discovery() -> OffsetApiDiscovery:
    return OffsetApiDiscovery()

def create_page_number_discovery() -> PageNumberDiscovery:
    return PageNumberDiscovery()

def create_rss_discovery() -> RssDiscovery:
    return RssDiscovery()

def create_sitemap_discovery() -> SitemapDiscovery:
    return SitemapDiscovery()