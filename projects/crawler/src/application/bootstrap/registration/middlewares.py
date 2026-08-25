from typing import Any

from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.cache.protocol import Cache
from core.cache.memory import MemoryCache
from core.request.middleware import (
    MiddlewareRegistry,
    MiddlewareManager,
    MiddlewareType,

    build_auth_middleware_factory,
    build_cache_middleware_factory,
    build_cookie_middleware_factory,
    build_deduplicate_middleware_factory,
    build_fingerprint_middleware_factory,
    build_proxy_middleware_factory,
    build_retry_middleware_factory,
    build_session_middleware_factory,
    build_throttle_middleware_factory,

    AuthProvider,
    BasicAuthProvider,
    AuthPolicy,

    CachePolicy,
    CacheKeyProvider,
    FingerprintCacheKeyProvider,

    CookiePolicy,
    DeduplicatePolicy,

    FingerprintProvider,
    DefaultFingerprintProvider,

    ProxyProvider,
    ProxyPolicy,

    RetryPolicy,

    SessionStore,
    MemorySessionStore,
    SessionPolicy,

    ThrottleLimiter,
    InMemoryThrottleLimiter,
    ThrottleKeyResolver,
    HostThrottleKeyResolver,
    ThrottlePolicy,
)
def register_middleware_dependencies(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        AuthProvider,
        BasicAuthProvider,
    )

    builder.add_type(
        AuthPolicy,
    )

    builder.add_type(
        Cache,
        MemoryCache,
    )

    builder.add_type(
        CachePolicy,
    )

    builder.add_type(
        CacheKeyProvider,
        FingerprintCacheKeyProvider,
    )

    builder.add_type(
        CookiePolicy,
    )

    builder.add_type(
        DeduplicatePolicy,
    )

    builder.add_type(
        FingerprintProvider,
        DefaultFingerprintProvider,
    )

    builder.add_type(
        ProxyProvider,
    )

    builder.add_type(
        ProxyPolicy,
    )

    builder.add_type(
        RetryPolicy,
    )

    builder.add_type(
        SessionStore,
        MemorySessionStore,
    )

    builder.add_type(
        SessionPolicy,
    )

    builder.add_type(
        ThrottleLimiter,
        InMemoryThrottleLimiter,
    )

    builder.add_type(
        ThrottleKeyResolver,
        HostThrottleKeyResolver,
    )

    builder.add_type(
        ThrottlePolicy,
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
        build_auth_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.CACHE,
        build_cache_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.COOKIE,
        build_cookie_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.DEDUPLICATE,
        build_deduplicate_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.FINGERPRINT,
        build_fingerprint_middleware_factory(
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
        MiddlewareType.RETRY,
        build_retry_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.SESSION,
        build_session_middleware_factory(
            resolver,
        ),
    )

    registry.register(
        MiddlewareType.THROTTLE,
        build_throttle_middleware_factory(
            resolver,
        ),
    )

    return registry