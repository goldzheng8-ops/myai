from typing import Any, Protocol

from core.cache.protocol import Cache
from core.provider import ProviderResolver
from core.request.middleware.auth.middleware import AuthMiddleware
from core.request.middleware.cache.middleware import CacheMiddleware
from core.request.middleware.cookie.middleware import CookieMiddleware
from core.request.middleware.deduplicate.middleware import DeduplicateMiddleware
from core.request.middleware.fingerprint.middleware import FingerprintMiddleware
from core.request.middleware.header.middleware import HeaderMiddleware
from core.request.middleware.proxy.middleware import ProxyMiddleware
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.proxy.resolver import ProxyProviderResolver
from core.request.middleware.response_validation.default_validator import DefaultResponseValidator
from core.request.middleware.response_validation.middleware import ResponseValidationMiddleware
from core.request.middleware.retry.middleware import RetryMiddleware
from core.request.middleware.retry.policy import RetryPolicy
from core.request.middleware.robot.middleware import RobotMiddleware
from core.request.middleware.robot.policy import RobotsPolicy
from core.request.middleware.session.middleware import SessionMiddleware
from core.request.middleware.throttle.middleware import ThrottleMiddleware
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.cache.key import CacheKeyProvider
from core.request.middleware.config import AuthMiddlewareConfig, CacheMiddlewareConfig, CookieMiddlewareConfig, DeduplicateMiddlewareConfig, FingerprintMiddlewareConfig, HeaderMiddlewareConfig, ProxyMiddlewareConfig, ResponseValidationMiddlewareConfig, RetryMiddlewareConfig, RobotMiddlewareConfig, SessionMiddlewareConfig, ThrottleMiddlewareConfig, UserAgentMiddlewareConfig
from core.request.middleware.fingerprint.provider import FingerprintProvider

from core.request.middleware.session.store import SessionStore
from core.request.middleware.throttle.limiter import ThrottleLimiter
from core.request.middleware.throttle.resolver import ThrottleKeyResolver
from core.request.middleware.user_agent.middleware import UserAgentMiddleware
from core.request.middleware.user_agent.resolver import UserAgentProviderResolver
from .base import MiddlewareConfigT

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

class HeaderMiddlewareFactory:
    def __call__(
        self,
        config: HeaderMiddlewareConfig,
    ) -> HeaderMiddleware:

        return HeaderMiddleware(
            config=config,
        )

class ResponseValidationMiddlewareFactory:
    def __call__(
        self,
        config: ResponseValidationMiddlewareConfig,
    ) -> ResponseValidationMiddleware:
        validator = DefaultResponseValidator(
            config,
        )

        return ResponseValidationMiddleware(
            validator=validator,
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


def build_proxy_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory[ProxyMiddlewareConfig]:

    proxy_resolver:ProxyProviderResolver = resolver.resolve(
        ProxyProviderResolver,
    )

    def factory(
        config: ProxyMiddlewareConfig,
    ) -> ProxyMiddleware:

        provider = proxy_resolver.resolve(
            config.provider,
        )

        return ProxyMiddleware(
            provider=provider,
            config=config,
        )

    return factory

def build_user_agent_middleware_factory(
    resolver: ProviderResolver[Any, Any],
) -> MiddlewareFactory[UserAgentMiddlewareConfig]:

    user_agent_resolver:UserAgentProviderResolver = resolver.resolve(
        UserAgentProviderResolver,
    )

    def factory(
        config: UserAgentMiddlewareConfig,
    ) -> UserAgentMiddleware:

        provider = user_agent_resolver.resolve(
            config.provider,
        )

        return UserAgentMiddleware(
            provider=provider,
            config=config,
        )

    return factory


class RobotMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver   

    def __call__(
        self,
        config: RobotMiddlewareConfig,
    ) -> RobotMiddleware:

        return RobotMiddleware(
            policy=self._resolver.resolve(
                RobotsPolicy,
            ),
            config=config,
        )

class RetryMiddlewareFactory:
    def __init__(
        self,
        resolver: ProviderResolver[Any, Any],
    ) -> None:
        self._resolver = resolver   

    def __call__(
        self,
        config: RetryMiddlewareConfig,
    ) -> RetryMiddleware:

        return RetryMiddleware(
            policy=self._resolver.resolve(
                RetryPolicy,
            ),
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

