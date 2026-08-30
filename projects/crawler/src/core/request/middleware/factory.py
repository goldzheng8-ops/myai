
from typing import Any, Protocol

from core.cache.protocol import Cache
from core.provider import ProviderResolver
from core.request.middleware import AuthMiddleware, CacheMiddleware, CookieMiddleware, DeduplicateMiddleware, FingerprintMiddleware, ProxyMiddleware, RequestMiddleware, RetryMiddleware, SessionMiddleware, ThrottleMiddleware
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.cache.key import CacheKeyProvider
from core.request.middleware.config import AuthMiddlewareConfig, CacheMiddlewareConfig, CookieMiddlewareConfig, DeduplicateMiddlewareConfig, FingerprintMiddlewareConfig, ProxyMiddlewareConfig, RetryMiddlewareConfig, SessionMiddlewareConfig, ThrottleMiddlewareConfig
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.middleware.proxy.provider import ProxyProvider
from core.request.middleware.session.store import SessionStore
from core.request.middleware.throttle.limiter import ThrottleLimiter
from core.request.middleware.throttle.resolver import ThrottleKeyResolver
from .typing import MiddlewareConfigT

class MiddlewareFactory(Protocol[MiddlewareConfigT]):
    def __call__(
        self,
        config: MiddlewareConfigT,
    ) -> RequestMiddleware[Any]:
        ...

class AuthMiddlewareFactory:

    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver

    def __call__(
        self,
        config: AuthMiddlewareConfig,
    ) -> AuthMiddleware:

        return AuthMiddleware(
            provider=self._resolver.resolve(
                AuthProvider,
            ),
            config=config,
        )
class CacheMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver
    def __call__(
        self,
        config: CacheMiddlewareConfig,
    ) -> CacheMiddleware:

        return CacheMiddleware(
            cache=self._resolver.resolve(
                Cache,
            ),
            key_provider=self._resolver.resolve(
                CacheKeyProvider,
            ),
            config=config,
        )

class CookieMiddlewareFactory:
    def __call__(
        self,
        config: CookieMiddlewareConfig,
    ) -> CookieMiddleware:

        return CookieMiddleware(
            config=config,
        )

class DeduplicateMiddlewareFactory:
    def __call__(
        self,
        config: DeduplicateMiddlewareConfig,
    ) -> DeduplicateMiddleware:

        return DeduplicateMiddleware(
            config=config,
        )

class FingerprintMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver 
    def __call__(
        self,    
        config: FingerprintMiddlewareConfig,
    ) -> FingerprintMiddleware:

        return FingerprintMiddleware(
            provider=self._resolver.resolve(
                FingerprintProvider,
            ),
            config=config,
        )


class ProxyMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver 
    def __call__(
        self,    
        config: ProxyMiddlewareConfig,
    ) -> ProxyMiddleware:

        return ProxyMiddleware(
            provider=self._resolver.resolve(
                ProxyProvider,
            ),
            config=config,
        )


class RetryMiddlewareFactory:

    def __call__(
        self,
        config: RetryMiddlewareConfig,
    ) -> RetryMiddleware:

        return RetryMiddleware(
            config=config,
        )
    
class SessionMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver    

    def __call__(
        self,
        config: SessionMiddlewareConfig,
    ) -> SessionMiddleware:

        return SessionMiddleware(
            store=self._resolver.resolve(
                SessionStore,
            ),

            config=config,
        )

class ThrottleMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver    

    def __call__(
        self,
        config: ThrottleMiddlewareConfig,
    ) -> ThrottleMiddleware:

        return ThrottleMiddleware(
            limiter=self._resolver.resolve(
                ThrottleLimiter,
            ),
            resolver=self._resolver.resolve(
                ThrottleKeyResolver,
            ),
            config=config,
        )

