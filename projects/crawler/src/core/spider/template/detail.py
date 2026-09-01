


from core.extraction.extractor.context import ExtractContext
from core.request.context import RequestContext


from ..config import DetailSpiderConfig
from ..context import SpiderContext

from ..typing import SpiderTemplate
from .base import SpiderStep, TemplateSpider

class TemplateDetailSpider(
    TemplateSpider[DetailSpiderConfig],
):

    plugin_type = SpiderTemplate.DETAIL



    async def process(
        self,
        context: SpiderContext[DetailSpiderConfig],
        request: RequestContext,
        extract_context: ExtractContext,
    ) -> SpiderStep:
        try:
            item = (
                await self.services.extract_engine.extract(
                    context.config.extraction,
                    extract_context,
                )
            )

            return SpiderStep(
                request=request,
                items=[item],
            )
        finally:
            await extract_context.response.close()