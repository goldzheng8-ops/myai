from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from core.lifecycle.protocol import LifecycleParticipant
from core.request.context import RequestContext
from core.request.middleware.cookie.model import Cookie
from core.request.typing import (
    RequestHeaders,
    RequestParams,

)

ConfigT = TypeVar(
    "ConfigT",
)

@dataclass(slots=True)
class AuthCredentials:

    headers: RequestHeaders = field(
        default_factory=dict,
    )

    cookies: tuple[Cookie, ...] = ()

    params: RequestParams = field(
        default_factory=dict,
    )


class AuthProvider(
    ABC,
    Generic[ConfigT],
):

    def __init__(
        self,
        config: ConfigT,
    ) -> None:
        self._config = config

    @property
    def config(self) -> ConfigT:
        return self._config

    @abstractmethod
    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        raise NotImplementedError


    async def close(self) -> None:
        ...


type AuthProviderMap = dict[
    str,
    AuthProvider[Any],
]

class BaseAuthProvider(
    AuthProvider[ConfigT],
    LifecycleParticipant,
):

    async def start(self) -> None:
        return None

    async def close(self) -> None:
        return None