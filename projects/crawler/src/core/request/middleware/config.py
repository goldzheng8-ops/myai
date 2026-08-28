from __future__ import annotations
from dataclasses import dataclass
from typing import Annotated, Literal

from core.request.middleware.typing import MiddlewareType
from pydantic import Field


@dataclass(frozen=True, slots=True)
class MiddlewareConfig:
    pass

@dataclass(frozen=True, slots=True)
class RetryMiddlewareConfig(MiddlewareConfig):
    max_retries: int = 3
    backoff: float = 1.0
class AuthMiddlewareConfig(MiddlewareConfig):
    pass
class CacheMiddlewareConfig(MiddlewareConfig):
    pass
class CookieMiddlewareConfig(MiddlewareConfig):
    pass
class DeduplicateMiddlewareConfig(MiddlewareConfig):
    pass
class FingerprintMiddlewareConfig(MiddlewareConfig):
    pass
class ProxyMiddlewareConfig(MiddlewareConfig):
    pass
class SessionMiddlewareConfig(MiddlewareConfig):
    pass
class ThrottleMiddlewareConfig(MiddlewareConfig):
    pass


@dataclass(frozen=True, slots=True)
class MiddlewareSpec:
    type: MiddlewareType
    enabled: bool = True
    priority: int = 0
    config: MiddlewareConfig | None = None

class RetryMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.RETRY] = (MiddlewareType.RETRY)
    config: RetryMiddlewareConfig 
class AuthMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.AUTH] = (MiddlewareType.AUTH)
    config: AuthMiddlewareConfig 
class CacheMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.CACHE] = (MiddlewareType.CACHE)
    config: CacheMiddlewareConfig 
class CookieMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.COOKIE] = (MiddlewareType.COOKIE)
    config: CookieMiddlewareConfig 
class DeduplicateMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.DEDUPLICATE] = (MiddlewareType.DEDUPLICATE)
    config: DeduplicateMiddlewareConfig 
class FingerprintMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.FINGERPRINT] = (MiddlewareType.FINGERPRINT)
    config: FingerprintMiddlewareConfig 
class ProxyMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.PROXY] = (MiddlewareType.PROXY)
    config: ProxyMiddlewareConfig 
class SessionMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.SESSION] = (MiddlewareType.SESSION)
    config: SessionMiddlewareConfig 
class ThrottleMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.THROTTLE] = (MiddlewareType.THROTTLE)
    config: ThrottleMiddlewareConfig 

MiddlewareSpecUnion = Annotated[
    (
        RetryMiddlewareSpec
        | AuthMiddlewareSpec
        | CacheMiddlewareSpec
        | CookieMiddlewareSpec
        | DeduplicateMiddlewareSpec
        | FingerprintMiddlewareSpec
        | ProxyMiddlewareSpec
        | SessionMiddlewareSpec
        | ThrottleMiddlewareSpec
    ),
    Field(discriminator="type"),
]