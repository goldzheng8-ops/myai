from __future__ import annotations

from abc import ABC, abstractmethod
from typing import  ClassVar, Generic,TypeVar


from core.extraction.extractor.context import ExtractContext
from core.plugin import Plugin
from core.request.context import RequestContext

from core.spider.step import SpiderStep

from ..config import SpiderConfig
from ..context import SpiderContext

from ..services import SpiderServices
from ..typing import SpiderTemplate


ConfigT = TypeVar(
    "ConfigT",
    bound=SpiderConfig,
)


class TemplateSpider(
    Plugin,
    Generic[ConfigT],
    ABC,
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
        context: SpiderContext[ConfigT],
        request: RequestContext,
        extract_context: ExtractContext,
    ) -> SpiderStep:

        raise NotImplementedError
    


    