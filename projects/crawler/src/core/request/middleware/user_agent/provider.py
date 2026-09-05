
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from core.request.context import RequestContext

ConfigT = TypeVar(
    "ConfigT",
)


class UserAgentProvider(
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
    ) -> str | None:
        raise NotImplementedError



type UserAgentProviderMap = dict[
    str,
    UserAgentProvider[Any],
]

