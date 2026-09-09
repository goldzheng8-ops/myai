from typing import Any

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.cache.protocol import Cache
from core.cache.memory import MemoryCache
from core.request.middleware.auth.basic import BasicAuthProvider
from core.request.middleware.auth.factory import AuthProviderFactory
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.auth.resolver import AuthProviderResolver
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

def register_auth_providers_resolver(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    def build_auth_provider_resolver(
        config: ApplicationConfig,
    ) -> AuthProviderResolver:

        providers = AuthProviderFactory().create_all(
            config.auth_providers,
        )

        return AuthProviderResolver(providers)
    builder.add_factory(
        AuthProviderResolver,
        lambda resolver: build_auth_provider_resolver(config),
)
    

def register_middleware_dependencies(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    throttle = config.runtime.throttle
    robots_policy=config.runtime.robots_policy
    retry_policy=config.runtime.retry_policy
    builder.add_type(
        AuthProvider,
        BasicAuthProvider,
    )

    builder.add_type(
        Cache,
        MemoryCache,
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