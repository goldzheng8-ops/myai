from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from core.request.context import RequestContext
from .config import ProxyConfig


ConfigT = TypeVar(
    "ConfigT",
)


class ProxyProvider(
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
    ) -> ProxyConfig  | None:
        raise NotImplementedError



type ProxyProviderMap = dict[
    str,
    ProxyProvider[Any],
]

