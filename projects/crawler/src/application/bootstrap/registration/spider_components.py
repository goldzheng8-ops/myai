from typing import Any

from core.provider import ProviderBuilder, ProviderResolver
from core.spider import (
    SpiderRegistry,
    build_api_spider_factory,
    build_browser_spider_factory,
    build_detail_spider_factory,
    build_list_spider_factory,
    SpiderTemplate,
)


def register_spider_components(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        SpiderRegistry,
        lambda resolver: create_spider_registry(
            resolver,
        ),
    )

def create_spider_registry(
    resolver: ProviderResolver[Any, Any],
) -> SpiderRegistry:

    registry = SpiderRegistry()

  
    registry.register(
        SpiderTemplate.API,
        build_api_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.BROWSER,
        build_browser_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.DETAIL,
        build_detail_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.LIST,
        build_list_spider_factory(
            resolver,
        ),
    )



    return registry