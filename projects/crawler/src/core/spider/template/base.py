from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Generic,TypeVar

from core.extraction.extractor.config import ExtractConfig
from core.extraction.extractor.context import ExtractContext
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
    Generic[ConfigT],
    ABC,
):

    template: ClassVar[SpiderTemplate]

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
    ) -> SpiderStep:

        raise NotImplementedError



    # async def _request(
    #     self,
    #     context: SpiderContext[ConfigT],
    #     request_context: RequestContext,
    # ) -> RequestContext:

    #     return await self._services.request_runner.run(
    #         request_context,
    #     )
    
    async def _extract_request(
        self,
        spider_context: SpiderContext[ConfigT],
        request_context: RequestContext,
        config: ExtractConfig,
    ) -> Any:

        extract_context = await self._execute_request(
            spider_context,
            request_context,
        )

        return await self.services.extract_engine.extract(
            config,
            extract_context,
        )

    async def _execute_request(
        self,
        context: SpiderContext[ConfigT],
        request_context: RequestContext,
    ) -> ExtractContext:

        request_context = await self._services.request_runner.run(
            request_context,
        )

        return self._build_extract_context(
            request_context,
        )
    def _build_extract_context(
        self,
        request_context: RequestContext,
    ) -> ExtractContext:

        result = request_context.result

        if result is None:
            raise RuntimeError(
                "Request execution produced no result.",
            )

        response = result.response

        if response is None:
            raise RuntimeError(
                "Request execution produced no response.",
            )

        adapter = (
            self._services
            .response_adapter_factory
            .create(response)
        )

        return ExtractContext(
            request=request_context,
            response=adapter,
            runtime=request_context.runtime,
        )