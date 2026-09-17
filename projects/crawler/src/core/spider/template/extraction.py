from core.extraction.extractor.context import ExtractContext
from core.output.model import OutputItem
from core.request.discovery.context import DiscoveryContext
from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import ExtractConSpiderConfig
from core.spider.template.base import RequestTemplate


class ExtractionRequestTemplate(
    RequestTemplate[ExtractConSpiderConfig],
):
    plugin_type = SpiderTemplate.EXTRACTION

    async def process(
        self,
        *,
        context: SpiderContext[ExtractConSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        extract_context = (
            self._build_extract_context(
                request,
            )
        )

        item = await self._extract(
            context=context,
            request=request,
            extract_context=extract_context,
        )

        requests = await self._discover(
            context,
            extract_context,
        )

        return RequestStep(
            request=request,
            item=item,
            outputs=context.config.outputs,
            requests=requests,
        )
    def _build_extract_context(
        self,
        request: RequestContext,
    ) -> ExtractContext:

        result = request.result

        if result is None:
            raise RuntimeError(
                "Request execution produced no result.",
            )

        return ExtractContext(
            request=request,
            response=result.response,
            runtime=request.runtime,
        )

    async def _extract(
        self,
        *,
        context: SpiderContext[ExtractConSpiderConfig],
        request: RequestContext,
        extract_context: ExtractContext,
    ) -> OutputItem:

        extract_result = (
            await self._services.extract_executor.extract(
                config=context.config.extraction,
                context=extract_context,
            )
        )
        return OutputItem(
            data=extract_result.data,
            spider=context.config.name,
            metadata=extract_result.metadata,
        )


    async def _discover(
        self,
        context: SpiderContext[ExtractConSpiderConfig],
        extract_context: ExtractContext,
    ) -> list[RequestDescriptor]:

        descriptors: list[RequestDescriptor] = []
        discovery_context=DiscoveryContext(
            request=extract_context.request,
            response=extract_context.response,
        )

        for config in context.config.discovery:
            result = (
                await self.services.discovery_engine.discover(
                    context=discovery_context,
                    config=config,
                )
            )

            descriptors.extend(
                record.descriptor
                for record in result.records
            )

        return descriptors

