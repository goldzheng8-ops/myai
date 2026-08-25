
from typing import Any, Protocol

from core.cache.protocol import Cache
from core.provider import ProviderResolver
from core.request.middleware import AuthMiddleware, CacheMiddleware, CookieMiddleware, DeduplicateMiddleware, FingerprintMiddleware, ProxyMiddleware, RequestMiddleware, RetryMiddleware, SessionMiddleware, ThrottleMiddleware
from core.request.middleware.auth.policy import AuthPolicy
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.cache.key import CacheKeyProvider
from core.request.middleware.cache.policy import CachePolicy
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.cookie.policy import CookiePolicy
from core.request.middleware.deduplicate.policy import DeduplicatePolicy
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.middleware.proxy.policy import ProxyPolicy
from core.request.middleware.proxy.provider import ProxyProvider
from core.request.middleware.retry.policy import RetryPolicy
from core.request.middleware.session.policy import SessionPolicy
from core.request.middleware.session.store import SessionStore
from core.request.middleware.throttle.limiter import ThrottleLimiter
from core.request.middleware.throttle.policy import ThrottlePolicy
from core.request.middleware.throttle.resolver import ThrottleKeyResolver


class MiddlewareFactory(Protocol):
    def __call__(
        self,
        config: MiddlewareConfig | None = None,
    ) -> RequestMiddleware:
        ...

def build_auth_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> AuthMiddleware:

        return AuthMiddleware(
            provider=resolver.resolve(
                AuthProvider,
            ),
            policy=resolver.resolve(
                AuthPolicy,
            ),
            config=config,
        )

    return factory
def build_cache_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> CacheMiddleware:

        return CacheMiddleware(
            cache=resolver.resolve(
                Cache,
            ),
            policy=resolver.resolve(
                CachePolicy,
            ),
            key_provider=resolver.resolve(
                CacheKeyProvider,
            ),
            config=config,
        )

    return factory
def build_cookie_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> CookieMiddleware:

        return CookieMiddleware(
            policy=resolver.resolve(
                CookiePolicy,
            ),
            config=config,
        )

    return factory
def build_deduplicate_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> DeduplicateMiddleware:

        return DeduplicateMiddleware(
            policy=resolver.resolve(
                DeduplicatePolicy,
            ),
            config=config,
        )

    return factory

def build_fingerprint_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> FingerprintMiddleware:

        return FingerprintMiddleware(
            provider=resolver.resolve(
                FingerprintProvider,
            ),
            config=config,
        )

    return factory
def build_proxy_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> ProxyMiddleware:

        return ProxyMiddleware(
            provider=resolver.resolve(
                ProxyProvider,
            ),
            policy=resolver.resolve(
                ProxyPolicy,
            ),
            config=config,
        )

    return factory
def build_retry_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> RetryMiddleware:

        return RetryMiddleware(
            policy=resolver.resolve(
                RetryPolicy,
            ),
            config=config,
        )

    return factory
def build_session_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> SessionMiddleware:

        return SessionMiddleware(
            store=resolver.resolve(
                SessionStore,
            ),
            policy=resolver.resolve(
                SessionPolicy,
            ),
            config=config,
        )

    return factory
def build_throttle_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> ThrottleMiddleware:

        return ThrottleMiddleware(
            limiter=resolver.resolve(
                ThrottleLimiter,
            ),
            resolver=resolver.resolve(
                ThrottleKeyResolver,
            ),
            policy=resolver.resolve(
                ThrottlePolicy,
            ),
            config=config,
        )

    return factory
