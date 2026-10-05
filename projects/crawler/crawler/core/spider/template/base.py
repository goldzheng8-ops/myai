from __future__ import annotations

from abc import abstractmethod
from typing import  ClassVar, Generic,TypeVar

from core.plugin import Plugin
from core.request.context import RequestContext
from core.spider.step import RequestStep
from ..config import SpiderConfig
from ..context import SpiderContext
from ..services import SpiderServices
from ..typing import SpiderTemplate


ConfigT = TypeVar(
    "ConfigT",
    bound=SpiderConfig,
)

class RequestTemplate(
    Plugin,
    Generic[ConfigT],
):

    plugin_type: ClassVar[SpiderTemplate]

    def __init__(
        self,
        services: SpiderServices,
    ) -> None:

        self._services = services

    @property
    def services(self) -> SpiderServices:
        return self._services

    @abstractmethod
    async def process(
        self,
        *,
        context: SpiderContext[ConfigT],
        request: RequestContext,
    ) -> RequestStep:

        raise NotImplementedError
    