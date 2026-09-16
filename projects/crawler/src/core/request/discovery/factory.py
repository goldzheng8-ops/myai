from collections.abc import Callable
from typing import Any, TypeAlias

from core.extraction.selector.executor import PipelineExecutor
from core.extraction.transform.executor import TransformExecutor
from core.provider import ProviderResolver
from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.plugins.cursor_api import CursorApiDiscovery
from core.request.discovery.plugins.html import HtmlDiscoveryPlugin
from core.request.discovery.plugins.infinite_scroll import InfiniteScrollDiscovery
from core.request.discovery.plugins.pagination import PaginationDiscoveryPlugin
from core.request.discovery.plugins.offset_api import OffsetApiDiscovery
from core.request.discovery.plugins.file import FileDiscoveryPlugin
from core.request.discovery.plugins.rss import RssDiscovery
from core.request.discovery.plugins.sitemap import SitemapDiscovery

DiscoveryFactory: TypeAlias = Callable[
    [],
    DiscoveryPlugin[Any],
]

def build_html_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> HtmlDiscoveryPlugin:
        return HtmlDiscoveryPlugin(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_pagination_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> PaginationDiscoveryPlugin:
        return PaginationDiscoveryPlugin(
            transform_executor=resolver.resolve(
                TransformExecutor,
            ),
            pipeline_executor=resolver.resolve(
                PipelineExecutor,
            ),
        )
    return factory

def build_file_discovery_factory(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryFactory:

    def factory() -> FileDiscoveryPlugin:
        return FileDiscoveryPlugin(
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

