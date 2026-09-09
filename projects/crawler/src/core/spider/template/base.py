from __future__ import annotations

from abc import abstractmethod
from typing import  ClassVar, Generic,TypeVar


from core.extraction.extractor.context import ExtractContext
from core.plugin import Plugin
from core.request.context import RequestContext

from core.request.descriptor import RequestDescriptor
from core.spider.step import SpiderStep

from ..config import DiscoverySpiderConfig, SpiderConfig
from ..context import SpiderContext

from ..services import SpiderServices
from ..typing import SpiderTemplate


ConfigT = TypeVar(
    "ConfigT",
    bound=SpiderConfig,
)
DiscoveryConfigT = TypeVar(
    "DiscoveryConfigT",
    bound=DiscoverySpiderConfig,
)

class TemplateSpider(
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
        context: SpiderContext[ConfigT],
        request: RequestContext,
        extract_context: ExtractContext,
    ) -> SpiderStep:

        raise NotImplementedError
    

class DiscoveryTemplateSpider(
    TemplateSpider[DiscoveryConfigT],
):
    async def _discover(
        self,
        context: SpiderContext[DiscoveryConfigT],
        extract_context: ExtractContext,
    ) -> list[RequestDescriptor]:

        descriptors: list[RequestDescriptor] = []

        for config in context.config.discovery:

            result = (
                await self.services.discovery_engine.discover(
                    response=extract_context.response,
                    context=extract_context.request,
                    config=config,
                )
            )

            descriptors.extend(
                record.descriptor
                for record in result.records
            )

        return descriptors

    async def process(
        self,
        context: SpiderContext[DiscoveryConfigT],
        request: RequestContext,
        extract_context: ExtractContext,
    ) -> SpiderStep:
        try:
            item = await self.services.extract_engine.extract(
                context.config.extraction,
                extract_context,
            )
            print(item)
            requests = await self._discover(
                context,
                extract_context,
            )

            return SpiderStep(
                request=request,
                items=[item],
                requests=requests,
            )
        finally:
            await extract_context.response.close()

