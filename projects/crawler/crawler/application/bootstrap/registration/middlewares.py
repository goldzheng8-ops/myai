from typing import Any

import httpx

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider.protocol import ProviderResolver
from core.provider.builder import ProviderBuilder
from core.cache.protocol import Cache
from core.cache.memory import MemoryCache
from core.request.middleware.auth.auth_provider.apikey import ApiKeyAuthProvider
from core.request.middleware.auth.auth_provider.base import AuthProvider
from core.request.middleware.auth.auth_provider.basic import BasicAuthProvider
from core.request.middleware.auth.auth_provider.bearer import BearerAuthProvider
from core.request.middleware.auth.auth_provider.config import (
    ApiKeyAuthProviderConfig,
    BasicAuthProviderConfig,
    BearerAuthProviderConfig,
    CookieAuthProviderConfig,
    OAuth2CredentialsProviderConfig,
)
from core.request.middleware.auth.auth_provider.cookie import CookieAuthProvider
from core.request.middleware.auth.auth_provider.oauth2.credentials import OAuth2CredentialsProvider, OAuth2TokenRefresher
from core.request.middleware.auth.auth_provider.oauth2.initial import BrowserOAuth2InitialTokenLoader, OAuth2InitialTokenLoader
from core.request.middleware.auth.auth_provider.oauth2.refresher import OAuth2TokenEndpointClient
from core.request.middleware.auth.auth_provider.oauth2.store import InMemoryOAuth2TokenStore, OAuth2TokenStore
from core.request.middleware.auth.auth_provider.registry import AuthProviderRegistry
from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider
from core.request.middleware.cache.key import CacheKeyProvider, FingerprintCacheKeyProvider
from core.request.middleware.chain_builder import MiddlewareChainBuilder
from core.request.middleware.factory import CacheMiddlewareFactory, CookieMiddlewareFactory, DeduplicateMiddlewareFactory, FingerprintMiddlewareFactory, HeaderMiddlewareFactory, ResponseValidationMiddlewareFactory,  RetryMiddlewareFactory, RobotMiddlewareFactory, SessionMiddlewareFactory, ThrottleMiddlewareFactory, build_auth_middleware_factory, build_proxy_middleware_factory, build_user_agent_middleware_factory
from core.request.middleware.fingerprint.provider import DefaultFingerprintProvider, FingerprintProvider
from core.request.middleware.manager import MiddlewareManager
from core.request.middleware.proxy.resolver import ProxyProviderResolver
from core.request.middleware.retry.policy import DefaultRetryPolicy, RetryPolicy
from core.request.middleware.robots.default_policy import DefaultRobotsPolicy
from core.request.middleware.robots.policy import RobotsPolicy
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.proxy.provider import ProxyProvider
from core.request.middleware.proxy.factory import ProxyProviderFactory
from core.request.middleware.registry import MiddlewareRegistry
from core.request.middleware.session.store import MemorySessionStore, SessionStore
from core.request.middleware.throttle.limiter import InMemoryThrottleLimiter, ThrottleLimiter
from core.request.middleware.throttle.resolver import HostThrottleKeyResolver, ThrottleKeyResolver
from core.request.middleware.user_agent.factory import UserAgentProviderFactory
from core.request.middleware.user_agent.resolver import UserAgentProviderResolver
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.provider.factory import FactoryProvider

def register_proxy_providers_resolver(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    def build_proxy_provider_resolver(
        config: ApplicationConfig,
    ) -> ProxyProviderResolver:

        providers = ProxyProviderFactory().create_all(
            config.proxies,
        )

        return ProxyProviderResolver(providers)
    builder.add_factory(
        ProxyProviderResolver,
        lambda resolver: build_proxy_provider_resolver(config),
)

def register_user_agent_providers_resolver(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    def build_user_agent_provider_resolver(
        config: ApplicationConfig,
    ) -> UserAgentProviderResolver:

        providers = UserAgentProviderFactory().create_all(
            config.user_agents,
        )

        return UserAgentProviderResolver(providers)
    builder.add_factory(
        UserAgentProviderResolver,
        lambda resolver: build_user_agent_provider_resolver(config),
)


    

def register_middleware_dependencies(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    throttle = config.runtime.throttle
    robots_policy=config.runtime.robots_policy
    retry_policy=config.runtime.retry_policy
    auth_provider_configs=config.auth_providers
    builder.add_type(
        AuthProvider,
        BasicAuthProvider,
    )

    builder.add_type(
        Cache,
        MemoryCache,
        strategy_cls=FactoryProvider,
    )


    builder.add_type(
        CacheKeyProvider,
        FingerprintCacheKeyProvider,
    )


    builder.add_type(
        FingerprintProvider,
        DefaultFingerprintProvider,
    )

    builder.add_type(
        ProxyProvider,
    )


    builder.add_type(
        SessionStore,
        MemorySessionStore,
    )

    builder.add_factory(
        ThrottleLimiter,
        lambda resolver: InMemoryThrottleLimiter(
            delay=throttle.delay,
            concurrency=throttle.concurrency,
        ),
    )

    builder.add_factory(
        RobotsPolicy,
        lambda resolver: DefaultRobotsPolicy(
            timeout=robots_policy.timeout,
            ttl=robots_policy.ttl,
            failure_strategy=robots_policy.failure_strategy,
            failure_ttl=robots_policy.failure_ttl,
        ),
    )

    builder.add_factory(
        RetryPolicy,
        lambda resolver: DefaultRetryPolicy(
            config=retry_policy,
        ),
    )

    builder.add_type(
        ThrottleKeyResolver,
        HostThrottleKeyResolver,
    )

    builder.add_factory(
        BrowserAuthStateProvider,
        lambda resolver: BrowserAuthStateProvider(
            browser_runtime=resolver.resolve(BrowserRuntimeManager),
        ),
    )
    builder.add_factory(
        httpx.AsyncClient,
        lambda resolver: httpx.AsyncClient(),
    )
    builder.add_factory(
        OAuth2TokenEndpointClient,
        lambda resolver: OAuth2TokenEndpointClient(
            client=resolver.resolve(httpx.AsyncClient),
            config=config.oauth2_token_endpoint,
        ),
    )
    builder.add_factory(
        OAuth2TokenStore,
        lambda resolver: InMemoryOAuth2TokenStore(),
    )
    builder.add_factory(
        OAuth2TokenRefresher,
        lambda resolver: OAuth2TokenRefresher(
            endpoint_client=resolver.resolve(OAuth2TokenEndpointClient),
            token_store=resolver.resolve(OAuth2TokenStore),
        ),
    )
    for provider_config in auth_provider_configs:
        match provider_config:
            case BasicAuthProviderConfig() as basic_config:
                builder.add_factory(
                    BasicAuthProvider,
                    lambda resolver: BasicAuthProvider(
                        config=basic_config,
                    ),
                )
            case BearerAuthProviderConfig() as bearer_config:
                builder.add_factory(
                    BearerAuthProvider,
                    lambda resolver: BearerAuthProvider(
                        auth_state_provider=resolver.resolve(BrowserAuthStateProvider),
                        config=bearer_config,
                    ),
                )
            case CookieAuthProviderConfig() as cookie_config:
                builder.add_factory(
                    CookieAuthProvider,
                    lambda resolver: CookieAuthProvider(
                        auth_state_provider=resolver.resolve(BrowserAuthStateProvider),
                        config=cookie_config,
                    ),
                )
            case OAuth2CredentialsProviderConfig() as oauth2_config:
                builder.add_factory(
                    OAuth2CredentialsProvider,
                    lambda resolver: OAuth2CredentialsProvider(
                        token_refresher=resolver.resolve(OAuth2TokenRefresher),
                        initial_token_loader=resolver.resolve(OAuth2InitialTokenLoader),
                        config=oauth2_config,
                    ),
                )
                builder.add_factory(
                    OAuth2InitialTokenLoader,
                    lambda resolver: BrowserOAuth2InitialTokenLoader(
                        auth_state_provider=resolver.resolve(BrowserAuthStateProvider),
                        config=oauth2_config,
                    ),
                )
            case ApiKeyAuthProviderConfig() as api_key_config:
                builder.add_factory(
                    ApiKeyAuthProvider,
                    lambda resolver: ApiKeyAuthProvider(
                        config=api_key_config,
                    ),
                )
            case _:
                raise TypeError(
                    "Unsupported auth provider type: "
                    f"{provider_config.type!r}",
                )

    builder.add_factory(
        AuthProviderRegistry,
        lambda resolver: create_auth_provider_registry(
            resolver,
        ),
    )
def register_middlewares(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        MiddlewareRegistry,
        lambda resolver: create_middleware_registry(
            resolver,
        ),
    )

    builder.add_factory(
        MiddlewareManager,
        lambda resolver: MiddlewareManager(
            registry=resolver.resolve(
                MiddlewareRegistry,
            ),
            lifecycle=resolver.resolve(
                LifecycleManager,
            ),
        ),
    )
    builder.add_factory(
        MiddlewareChainBuilder,
        lambda resolver: MiddlewareChainBuilder(
            manager=resolver.resolve(
                MiddlewareManager,
            ),
        ),
    )

def create_middleware_registry(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareRegistry:

    registry = MiddlewareRegistry()

    registry.register(
        MiddlewareType.CACHE,
        CacheMiddlewareFactory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.COOKIE,
        CookieMiddlewareFactory(),
    )

    registry.register(
        MiddlewareType.DEDUPLICATE,
        DeduplicateMiddlewareFactory(),
    )

    registry.register(
        MiddlewareType.HEADER,
        HeaderMiddlewareFactory(),
    )

    registry.register(
        MiddlewareType.RESPONSE_VALIDATION,
        ResponseValidationMiddlewareFactory(),
    )

    registry.register(
        MiddlewareType.FINGERPRINT,
        FingerprintMiddlewareFactory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.AUTH,
        build_auth_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.PROXY,
        build_proxy_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.USER_AGENT,
        build_user_agent_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.RETRY,
        RetryMiddlewareFactory(resolver),
    )

    registry.register(
        MiddlewareType.ROBOT,
        RobotMiddlewareFactory(resolver),
    )

    registry.register(
        MiddlewareType.SESSION,
        SessionMiddlewareFactory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.THROTTLE,
        ThrottleMiddlewareFactory(
            resolver,
        ),
    )

    return registry

def create_auth_provider_registry(
    resolver: ProviderResolver[Any, Any],
) -> AuthProviderRegistry:
    registry = AuthProviderRegistry()

    registry.register(
        "basic",
        lambda : resolver.resolve(
            BasicAuthProvider,
        ),
    )
    registry.register(
        "bearer",
        lambda : resolver.resolve(
            BearerAuthProvider,
        ),
    )
    registry.register(
        "cookie",
        lambda : resolver.resolve(
            CookieAuthProvider,
        ),
    )
    registry.register(
        "oauth2",
        lambda : resolver.resolve(
            OAuth2CredentialsProvider,
        ),
    )

    return registry
