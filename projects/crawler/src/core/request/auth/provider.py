from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol

from core.request.context import RequestContext

@dataclass(slots=True)
class AuthCredentials:

    headers: dict[str, str] = field(
        default_factory=dict,
    )

    cookies: dict[str, str] = field(
        default_factory=dict,
    )

    params: dict[str, str] = field(
        default_factory=dict,
    )

class AuthProvider(Protocol):

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials | None:
        ...