from __future__ import annotations
from typing import Annotated, ClassVar, Literal

from core.request.typing import HttpMethod
from core.request.middleware.typing import MiddlewareType
from core.typing.config import BaseConfig
from pydantic import Field



class MiddlewareConfig(BaseConfig):
    pass

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


class AuthMiddlewareConfig(MiddlewareConfig):
    override_headers: bool = False
    override_cookies: bool = False
    override_params: bool = False


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

class CookieMiddlewareConfig(
    MiddlewareConfig,
):
    merge_session_cookies: bool = True
    update_session_cookies: bool = True

class DeduplicateMiddlewareConfig(
    MiddlewareConfig,
):
    pass

class FingerprintMiddlewareConfig(
    MiddlewareConfig,
):
    pass

class ProxyMiddlewareConfig(
    MiddlewareConfig,
):
    provider: str = "default"
    override: bool = False

class UserAgentMiddlewareConfig(MiddlewareConfig):
    provider: str = "default"
    override: bool = False

class HeaderMiddlewareConfig(MiddlewareConfig):
    headers: dict[str, str] = Field(
        default_factory=dict,
    )
    override: bool = False

class RobotMiddlewareConfig(
    MiddlewareConfig,
):
    user_agent: str | None = None

class SessionMiddlewareConfig(
    MiddlewareConfig,
):
    default_session_id: str | None = None
    create_if_missing: bool = True
    save_after_request: bool = True

class ThrottleMiddlewareConfig(
    MiddlewareConfig,
):
    pass

class ResponseValidationMiddlewareConfig(
    MiddlewareConfig,
):
    status_codes: frozenset[int] | None = None
    content_types: frozenset[str] | None = None
    min_body_size: int | None = None
    max_body_size: int | None = None

class MiddlewareSpec(BaseConfig):
    enabled: bool = True
    priority: ClassVar[int]


class RetryMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.RETRY] = (MiddlewareType.RETRY)
    priority: ClassVar[int] = 25
    config: RetryMiddlewareConfig = Field(
        default_factory=RetryMiddlewareConfig,
    ) 

class AuthMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.AUTH] = MiddlewareType.AUTH
    priority: ClassVar[int] = 45
    config: AuthMiddlewareConfig = Field(
        default_factory=AuthMiddlewareConfig,
    )
class CacheMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.CACHE] = (MiddlewareType.CACHE)
    priority: ClassVar[int] = 80
    config: CacheMiddlewareConfig = Field(
        default_factory=CacheMiddlewareConfig,
    ) 
class CookieMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.COOKIE] = (MiddlewareType.COOKIE)
    priority: ClassVar[int] = 60
    config: CookieMiddlewareConfig = Field(
        default_factory=CookieMiddlewareConfig,
    ) 
class DeduplicateMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.DEDUPLICATE] = (MiddlewareType.DEDUPLICATE)
    priority: ClassVar[int] = 90
    config: DeduplicateMiddlewareConfig = Field(
        default_factory=DeduplicateMiddlewareConfig,
    ) 
class FingerprintMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.FINGERPRINT] = (MiddlewareType.FINGERPRINT)
    priority: ClassVar[int] = 100
    config: FingerprintMiddlewareConfig = Field(
        default_factory=FingerprintMiddlewareConfig,
    ) 
class ProxyMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.PROXY] = (MiddlewareType.PROXY)
    priority: ClassVar[int] = 40
    config: ProxyMiddlewareConfig = Field(
        default_factory=ProxyMiddlewareConfig,
    ) 
class UserAgentMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.USER_AGENT] = (MiddlewareType.USER_AGENT)
    priority: ClassVar[int] = 50
    config: UserAgentMiddlewareConfig = Field(
        default_factory=UserAgentMiddlewareConfig,
    ) 
class HeaderMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.HEADER] = (MiddlewareType.HEADER)
    priority: ClassVar[int] = 55
    config: HeaderMiddlewareConfig = Field(
        default_factory=HeaderMiddlewareConfig,
    ) 
class RobotMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.ROBOT] = (MiddlewareType.ROBOT)
    priority: ClassVar[int] = 30
    config: RobotMiddlewareConfig = Field(
        default_factory=RobotMiddlewareConfig,
    ) 
    
class SessionMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.SESSION] = (MiddlewareType.SESSION)
    priority: ClassVar[int] = 70
    config: SessionMiddlewareConfig = Field(
        default_factory=SessionMiddlewareConfig,
    ) 
class ThrottleMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.THROTTLE] = (MiddlewareType.THROTTLE)
    priority: ClassVar[int] = 20
    config: ThrottleMiddlewareConfig = Field(
        default_factory=ThrottleMiddlewareConfig,
    ) 
class ResponseValidationMiddlewareSpec(MiddlewareSpec):
    type: Literal[MiddlewareType.RESPONSE_VALIDATION] = (MiddlewareType.RESPONSE_VALIDATION)
    priority: ClassVar[int] = 35
    config: ResponseValidationMiddlewareConfig = Field(
        default_factory=ResponseValidationMiddlewareConfig,
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
        | RobotMiddlewareSpec
        | SessionMiddlewareSpec
        | ThrottleMiddlewareSpec
        | UserAgentMiddlewareSpec
        | HeaderMiddlewareSpec
        | ResponseValidationMiddlewareSpec
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
    | RobotMiddlewareConfig
    | SessionMiddlewareConfig
    | ThrottleMiddlewareConfig
    | UserAgentMiddlewareConfig
    | HeaderMiddlewareConfig
    | ResponseValidationMiddlewareConfig
)