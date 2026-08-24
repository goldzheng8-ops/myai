
from enum import Enum
from typing import  TypeAlias,TYPE_CHECKING
from collections.abc import Awaitable, Callable



if TYPE_CHECKING :
    from core.request.context import RequestContext


RequestMiddlewareNext: TypeAlias = Callable[
    [RequestContext],
    Awaitable[RequestContext],
]

class MiddlewareType(str,Enum):
    FINGERPRINT = "fingerprint"
    RETRY = "retry"
    AUTH = "auth"
    CACHE = "cache"
    DEDUPLICATE = "deduplicate"
    PROXY = "proxy"
    SESSION = "session"
    COOKIE = "cookie"
    THROTTLE = "throttle"