from __future__ import annotations
from dataclasses import dataclass, field
from typing import Annotated, Literal

from core.request.typing import HttpMethod
from core.request.middleware.typing import MiddlewareType
from pydantic import Field


@dataclass(frozen=True, slots=True)
class MiddlewareConfig:
    pass

@dataclass(frozen=True, slots=True)
class RetryMiddlewareConfig(
    MiddlewareConfig,
):
    max_retries: int = 3
    retry_delay: float = 1.0
    backoff_factor: float = 1.0
    max_delay: float | None = None
    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError(
                "max_retries must be greater than or equal to 0."
            )
        if self.retry_delay < 0:
            raise ValueError(
                "retry_delay must be greater than or equal to 0."
            )
        if self.backoff_factor <= 0:
            raise ValueError(
                "backoff_factor must be greater than 0."
            )
        if (
            self.max_delay is not None
            and self.max_delay < 0
        ):
            raise ValueError(
                "max_delay must be greater than or equal to 0."
            )

@dataclass(frozen=True, slots=True)
class AuthMiddlewareConfig(MiddlewareConfig):
    override_headers: bool = False
    override_cookies: bool = False
    override_params: bool = False

@dataclass(frozen=True, slots=True)
class CacheMiddlewareConfig(
    MiddlewareConfig,
):
    read: bool = True
    write: bool = True
    methods: frozenset[HttpMethod] = frozenset(
        {
            HttpMethod.GET,
            HttpMethod.HEAD,
        }
    )
@dataclass(frozen=True, slots=True)
class CookieMiddlewareConfig(
    MiddlewareConfig,
):
    merge_session_cookies: bool = True
    update_session_cookies: bool = True
@dataclass(frozen=True, slots=True)
class DeduplicateMiddlewareConfig(
    MiddlewareConfig,
):
    pass
@dataclass(frozen=True, slots=True)
class FingerprintMiddlewareConfig(
    MiddlewareConfig,
):
    pass
@dataclass(frozen=True, slots=True)
class ProxyMiddlewareConfig(
    MiddlewareConfig,
):
    override: bool = False
@dataclass(frozen=True, slots=True)
class SessionMiddlewareConfig(
    MiddlewareConfig,
):
    default_session_id: str | None = None
    create_if_missing: bool = True
    save_after_request: bool = True
@dataclass(frozen=True, slots=True)
class ThrottleMiddlewareConfig(
    MiddlewareConfig,
):
    pass


@dataclass(frozen=True, slots=True)
class MiddlewareSpec:
    type: MiddlewareType
    enabled: bool = True
    priority: int = 0
    config: MiddlewareConfig | None = None

class RetryMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.RETRY] = (MiddlewareType.RETRY)
    config: RetryMiddlewareConfig = field(
        default_factory=RetryMiddlewareConfig,
    ) 
@dataclass(frozen=True, slots=True)
class AuthMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.AUTH] = MiddlewareType.AUTH
    config: AuthMiddlewareConfig = field(
        default_factory=AuthMiddlewareConfig,
    )
class CacheMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.CACHE] = (MiddlewareType.CACHE)
    config: CacheMiddlewareConfig = field(
        default_factory=CacheMiddlewareConfig,
    ) 
class CookieMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.COOKIE] = (MiddlewareType.COOKIE)
    config: CookieMiddlewareConfig = field(
        default_factory=CookieMiddlewareConfig,
    ) 
class DeduplicateMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.DEDUPLICATE] = (MiddlewareType.DEDUPLICATE)
    config: DeduplicateMiddlewareConfig = field(
        default_factory=DeduplicateMiddlewareConfig,
    ) 
class FingerprintMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.FINGERPRINT] = (MiddlewareType.FINGERPRINT)
    config: FingerprintMiddlewareConfig = field(
        default_factory=FingerprintMiddlewareConfig,
    ) 
class ProxyMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.PROXY] = (MiddlewareType.PROXY)
    config: ProxyMiddlewareConfig = field(
        default_factory=ProxyMiddlewareConfig,
    ) 
class SessionMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.SESSION] = (MiddlewareType.SESSION)
    config: SessionMiddlewareConfig = field(
        default_factory=SessionMiddlewareConfig,
    ) 
class ThrottleMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.THROTTLE] = (MiddlewareType.THROTTLE)
    config: ThrottleMiddlewareConfig = field(
        default_factory=ThrottleMiddlewareConfig,
    ) 

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

MiddlewareConfigUnion = (
    RetryMiddlewareConfig
    | AuthMiddlewareConfig
    | CacheMiddlewareConfig
    | CookieMiddlewareConfig
    | DeduplicateMiddlewareConfig
    | FingerprintMiddlewareConfig
    | ProxyMiddlewareConfig
    | SessionMiddlewareConfig
    | ThrottleMiddlewareConfig
)