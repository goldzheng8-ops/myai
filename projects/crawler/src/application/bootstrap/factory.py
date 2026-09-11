from __future__ import annotations

from application.bootstrap.registration.outputs import register_outputs
from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.output.resolver import OutputResolver
from core.provider import (
    ProviderBuilder,
    SingletonProvider,
)
from core.request.middleware.auth.resolver import AuthProviderResolver

from .container import ApplicationContainer
from .registration import (
    register_adapters,
    register_crawler,
    register_discoveries,
    register_downloaders,
    register_events,
    register_extractors,
    register_lifecycle,
    register_proxy_providers_resolver,
    register_user_agent_providers_resolver,
    register_auth_providers_resolver,
    register_middleware_dependencies,
    register_middlewares,
    register_runtimes,
    register_request_services,
    register_resolvers,
    register_selector_registries,
    register_spider_components,
    register_spider_configs,
    register_template,
    register_transforms,
)

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

        container = ApplicationContainer(providers)

        self._register_lifecycle_participants(
            container,
            config,
        )

        return container

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
        register_proxy_providers_resolver(
            builder,
            config,          
        )
        register_user_agent_providers_resolver(
            builder,
            config,          
        )
        register_auth_providers_resolver(
            builder,
            config,          
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

        register_template(
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
        register_outputs(builder, config)
        register_request_services(
            builder,
        )

        register_crawler(
            builder,
            config,
        )

    def _register_lifecycle_participants(
        self,
        container: ApplicationContainer,
        config: ApplicationConfig,
    ) -> None:

        lifecycle = container.resolve(
            LifecycleManager,
        )

        auth_resolver:AuthProviderResolver = container.resolve(
            AuthProviderResolver,
        )

        for provider in auth_resolver.values():
            lifecycle.register(provider)

        out_resolver:OutputResolver = container.resolve(
            OutputResolver,
        )

        for output_sink in out_resolver.values():
            lifecycle.register(output_sink)
