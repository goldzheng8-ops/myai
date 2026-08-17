from core.extraction.extractor.context import ExtractContext
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor


from ..config import ApiSpiderConfig
from ..context import SpiderContext

from ..typing import SpiderTemplate
from .base import SpiderStep, TemplateSpider

class TemplateApiSpider(
    TemplateSpider[ApiSpiderConfig],
):

    template = SpiderTemplate.API



    async def process(
        self,
        context: SpiderContext[ApiSpiderConfig],
        request: RequestContext,
        extract_context: ExtractContext, 
    ) -> SpiderStep:

        item = (
            await self.services.extract_engine.extract(
                context.config.extraction,
                extract_context,
            )
        )

        requests = await self._discover(
            context,
            extract_context,
        )

        return SpiderStep(
            request=request,
            items=[item],
            requests=requests,
        )

    async def _discover(
        self,
        context: SpiderContext[ApiSpiderConfig],
        extract_context: ExtractContext,
    ) -> list[RequestDescriptor]:

        descriptors: list[RequestDescriptor] = []

        for config in context.config.discovery:

            discovery_result = (
                await self.services.discovery_engine.discover(
                    response=extract_context.response,
                    context=extract_context.request,
                    config=config,
                )
            )

            descriptors.extend(
                record.descriptor
                for record
                in discovery_result.records
            )

        return descriptors