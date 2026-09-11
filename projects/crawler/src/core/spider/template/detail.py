


from core.extraction.extractor.context import ExtractContext
from core.output.model import OutputItem
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

        item = (
            await self.services.extract_engine.extract(
                context.config.extraction,
                extract_context,
            )
        )

        return SpiderStep(
            request=request,
            item=OutputItem(
                data=item.data,
                spider=context.config.name,
                metadata=item.metadata
            ),
            outputs=context.config.outputs,
        )
