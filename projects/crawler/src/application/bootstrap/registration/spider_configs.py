from application.config.model import ApplicationConfig
from application.config.registry import SpiderConfigRegistry
from core.provider import ProviderBuilder

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