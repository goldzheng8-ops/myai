from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol

from core.request.context import RequestContext
from core.request.typing import (
    RequestHeaders,
    RequestCookies,
    RequestParams,

)

@dataclass(slots=True)
class AuthCredentials:

    headers: RequestHeaders = field(
        default_factory=dict,
    )

    cookies: RequestCookies = field(
        default_factory=dict,
    )

    params: RequestParams = field(
        default_factory=dict,
    )

class AuthProvider(Protocol):

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials | None:
        ...