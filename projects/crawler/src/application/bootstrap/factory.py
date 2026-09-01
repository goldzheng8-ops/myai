from __future__ import annotations

from application.config.model import ApplicationConfig
from core.provider import (
    ProviderBuilder,
    SingletonProvider,
)

from .container import ApplicationContainer
from .registration.downloaders import register_downloaders
from .registration.middlewares import register_middleware_dependencies,register_middlewares
from .registration.spider_components import register_spider_components
from .registration.spider_configs import register_spider_configs
from .registration.runtimes import register_runtimes
from .registration.adapters import register_adapters
from .registration.extraction_services import register_extraction_services
from .registration.spider_services import register_spider_services
from .registration.lifecycle import register_lifecycle
from .registration.crawler import register_crawler
from .registration.request_services import register_request_services
from .registration.events import register_events
from .registration.resolvers import register_resolvers
from .registration.transforms import register_transforms
from .registration.extractors import register_extractors
from .registration.discoveries import register_discoveries
from .registration.selector import register_selector_registries

class ApplicationContainerFactory:
    """
    Composition root of the application.

    Builds the complete application dependency graph
    using the frozen core Provider system.
    """

    def create(
        self,
        config: ApplicationConfig,
    ) -> ApplicationContainer:

        builder = ProviderBuilder(
            strategy_cls=SingletonProvider,
        )

        self._register_application_services(
            builder,
            config,
        )

        providers = builder.build()

        return ApplicationContainer(
            providers,
        )

    def _register_application_services(
        self,
        builder: ProviderBuilder,
        config: ApplicationConfig,
    ) -> None:
        
        register_lifecycle(
            builder,
        )
        register_events(
            builder,
        )

        register_spider_configs(
            builder,
            config,
        )
        
        register_spider_components(
            builder,
        )

        register_adapters(
            builder,
        )

        register_runtimes(
            builder,
            config,
        )

        register_downloaders(
            builder,
        )

        register_middleware_dependencies(
            builder,
            config,
        )

        register_middlewares(
            builder,
        )

        register_selector_registries(
            builder,
        )

        register_resolvers(
            builder,
        )

        register_transforms(
            builder,
        )

        register_extractors(
            builder,
        )

        register_discoveries(
            builder,
        )

        register_request_services(
            builder,
        )

        register_extraction_services(
            builder,
        )

        register_spider_services(
            builder,
        )

        register_crawler(
            builder,
            config,
        )












