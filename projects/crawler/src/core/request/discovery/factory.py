from collections.abc import Callable
from typing import Any, TypeAlias

from core.extraction.selector.executor import PipelineExecutor
from core.extraction.transform.executor import TransformExecutor
from core.provider import ProviderResolver
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

def build_detail_link_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> DetailLinkDiscovery:
        return DetailLinkDiscovery(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_next_page_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> NextPageDiscovery:
        return NextPageDiscovery(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_page_number_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> PageNumberDiscovery:
        return PageNumberDiscovery(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_rss_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> RssDiscovery:
        return RssDiscovery(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_sitemap_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> SitemapDiscovery:
        return SitemapDiscovery(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def create_cursor_api_discovery() -> CursorApiDiscovery:
    return CursorApiDiscovery()

def create_infinite_scroll_discovery() -> InfiniteScrollDiscovery:
    return InfiniteScrollDiscovery()

def create_offset_api_discovery() -> OffsetApiDiscovery:
    return OffsetApiDiscovery()

