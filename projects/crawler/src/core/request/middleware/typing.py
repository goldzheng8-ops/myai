from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.request.context import RequestContext
from enum import Enum
from typing import TypeAlias
from collections.abc import Awaitable, Callable




RequestMiddlewareNext: TypeAlias = Callable[
    ["RequestContext"],
    Awaitable["RequestContext"],
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
    USER_AGENT = "user_agent"
    HEADER = "header"
    ROBOT = "robot"

