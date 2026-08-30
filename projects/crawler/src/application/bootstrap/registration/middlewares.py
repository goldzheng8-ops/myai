from typing import Any

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.cache.protocol import Cache
from core.cache.memory import MemoryCache
from core.request.middleware import (
    MiddlewareRegistry,
    MiddlewareManager,
    MiddlewareType,
    RetryMiddlewareFactory,
    AuthMiddlewareFactory,
    CacheMiddlewareFactory,
    CookieMiddlewareFactory,
    DeduplicateMiddlewareFactory,
    FingerprintMiddlewareFactory,
    ProxyMiddlewareFactory,
    SessionMiddlewareFactory,
    ThrottleMiddlewareFactory,

    AuthProvider,
    BasicAuthProvider,
    CacheKeyProvider,
    FingerprintCacheKeyProvider,
    FingerprintProvider,
    DefaultFingerprintProvider,
    ProxyProvider,
    SessionStore,
    MemorySessionStore,
    ThrottleLimiter,
    InMemoryThrottleLimiter,
    ThrottleKeyResolver,
    HostThrottleKeyResolver,
)
def register_middleware_dependencies(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:
    throttle = config.runtime.throttle
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
        MiddlewareType.FINGERPRINT,
        FingerprintMiddlewareFactory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.PROXY,
        ProxyMiddlewareFactory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.RETRY,
        RetryMiddlewareFactory(),
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