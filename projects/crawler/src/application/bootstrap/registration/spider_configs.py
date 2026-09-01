from application.config.model import ApplicationConfig
from application.config.registry import SpiderConfigRegistry
from core.provider import ProviderBuilder
from application.config.merger import ConfigMerger
from application.config.resolver import SpiderConfigResolver

def register_spider_configs(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    registry = SpiderConfigRegistry(
        config,
    )

    builder.add_instance(
        SpiderConfigRegistry,
        registry,
    )
    # Register config merger and resolver used by the crawler services
    builder.add_type(
        ConfigMerger,
    )

    builder.add_factory(
        SpiderConfigResolver,
        lambda resolver: SpiderConfigResolver(
            resolver.resolve(
                ConfigMerger,
            ),
        ),
    )