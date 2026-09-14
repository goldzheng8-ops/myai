from typing import Any

from core.provider import ProviderBuilder, ProviderResolver
from core.request.discovery.engine import DiscoveryEngine
from core.request.discovery.registry import DiscoveryRegistry
from core.request.discovery.typing import DiscoveryType
from core.request.discovery.factory import (
    create_cursor_api_discovery,
    create_infinite_scroll_discovery,
    create_offset_api_discovery,
    build_detail_link_discovery_factory,
    build_next_page_discovery_factory,
    build_page_number_discovery_factory,
    build_rss_discovery_factory,
    build_sitemap_discovery_factory,
)


def register_discoveries(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        DiscoveryEngine,
        lambda resolver: DiscoveryEngine(
            registry=resolver.resolve(
                DiscoveryRegistry,
            ),
        ),
    )

    builder.add_factory(
        DiscoveryRegistry,
        lambda resolver: create_discovery_registry(
            resolver,
        ),
    )


def create_discovery_registry(
    resolver: ProviderResolver[Any, Any],
) -> DiscoveryRegistry:

    registry = DiscoveryRegistry()

    registry.register(
        DiscoveryType.CURSOR_API,
        create_cursor_api_discovery,
    )

    registry.register(
        DiscoveryType.INFINITE_SCROLL,
        create_infinite_scroll_discovery,
    )

    registry.register(
        DiscoveryType.OFFSET_API,
        create_offset_api_discovery,
    )

    registry.register(
        DiscoveryType.DETAIL_LINK,
        build_detail_link_discovery_factory(resolver),
    )

    registry.register(
        DiscoveryType.NEXT_PAGE,
        build_next_page_discovery_factory(resolver),
    )

    registry.register(
        DiscoveryType.PAGE_NUMBER,
        build_page_number_discovery_factory(resolver),
    )

    registry.register(
        DiscoveryType.RSS,
        build_rss_discovery_factory(resolver),
    )

    registry.register(
        DiscoveryType.SITEMAP,
        build_sitemap_discovery_factory(resolver),
    )


    return registry