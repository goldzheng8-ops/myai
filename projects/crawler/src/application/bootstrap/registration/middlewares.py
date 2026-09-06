from typing import Any

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.cache.protocol import Cache
from core.cache.memory import MemoryCache
from core.request.middleware.auth.basic import BasicAuthProvider
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.cache.key import CacheKeyProvider, FingerprintCacheKeyProvider
from core.request.middleware.factory import AuthMiddlewareFactory, CacheMiddlewareFactory, CookieMiddlewareFactory, DeduplicateMiddlewareFactory, FingerprintMiddlewareFactory, HeaderMiddlewareFactory,  RetryMiddlewareFactory, RobotMiddlewareFactory, SessionMiddlewareFactory, ThrottleMiddlewareFactory, build_proxy_middleware_factory, build_user_agent_middleware_factory
from core.request.middleware.fingerprint.provider import DefaultFingerprintProvider, FingerprintProvider
from core.request.middleware.manager import MiddlewareManager
from core.request.middleware.proxy.resolver import ProxyProviderResolver
from core.request.middleware.retry.policy import RetryPolicy
from core.request.middleware.robot.default_policy import DefaultRobotsPolicy
from core.request.middleware.robot.policy import RobotsPolicy
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.proxy.provider import ProxyProvider
from core.request.middleware.proxy.factory import ProxyProviderFactory
from core.request.middleware.registry import MiddlewareRegistry
from core.request.middleware.session.store import MemorySessionStore, SessionStore
from core.request.middleware.throttle.limiter import InMemoryThrottleLimiter, ThrottleLimiter
from core.request.middleware.throttle.resolver import HostThrottleKeyResolver, ThrottleKeyResolver
from core.request.middleware.user_agent.factory import UserAgentProviderFactory
from core.request.middleware.user_agent.resolver import UserAgentProviderResolver

def register_proxy_providers(
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

def register_user_agent_providers(
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
    robot=config.runtime.robot
    builder.add_type(
        AuthProvider,
        BasicAuthProvider,
    )

    builder.add_type(
        Cache,
        MemoryCache,
    )

    builder.add_type(
        RetryPolicy,
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
            timeout=robot.timeout,
            ttl=robot.ttl,
            failure_strategy=robot.failure_strategy,
            failure_ttl=robot.failure_ttl,
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

def create_middleware_registry(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareRegistry:

    registry = MiddlewareRegistry()

    registry.register(
        MiddlewareType.AUTH,
        AuthMiddlewareFactory(
            resolver,
        ),
    )

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
        MiddlewareType.FINGERPRINT,
        FingerprintMiddlewareFactory(
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