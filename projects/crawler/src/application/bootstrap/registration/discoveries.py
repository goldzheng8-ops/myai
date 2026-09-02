from typing import Any

from core.provider import ProviderBuilder, ProviderResolver
from core.request.discovery.engine import DiscoveryEngine
from core.request.discovery.typing import DiscoveryType
from core.request.discovery import (
    DiscoveryRegistry,
    create_cursor_api_discovery,
    create_detail_link_discovery,
    create_infinite_scroll_discovery,
    create_next_page_discovery,
    create_offset_api_discovery,
    create_page_number_discovery,
    create_rss_discovery,
    create_sitemap_discovery,
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
        DiscoveryType.DETAIL_LINK,
        create_detail_link_discovery,
    )

    registry.register(
        DiscoveryType.INFINITE_SCROLL,
        create_infinite_scroll_discovery,
    )

    registry.register(
        DiscoveryType.NEXT_PAGE,
        create_next_page_discovery,
    )

    registry.register(
        DiscoveryType.OFFSET_API,
        create_offset_api_discovery,
    )

    registry.register(
        DiscoveryType.PAGE_NUMBER,
        create_page_number_discovery,
    )

    registry.register(
        DiscoveryType.RSS,
        create_rss_discovery,
    )

    registry.register(
        DiscoveryType.SITEMAP,
        create_sitemap_discovery,
    )



    return registry