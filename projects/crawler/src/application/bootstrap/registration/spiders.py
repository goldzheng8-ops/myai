from typing import Any

from application.config.model import ApplicationConfig

from core.provider import ProviderBuilder, ProviderResolver

from core.spider import (
    SpiderRegistry,
    build_spider_factory,
)


def register_spiders(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        SpiderRegistry,
        lambda resolver: create_spider_registry(
            resolver,
            config,
        ),
    )

def create_spider_registry(
    resolver: ProviderResolver[Any, Any],
    config: ApplicationConfig,
) -> SpiderRegistry:

    registry = SpiderRegistry()

    for definition in config.spiders:
        registry.register(
            definition.template,
            build_spider_factory(
                resolver,
                definition.spider_type,
            ),
        )

    return registry