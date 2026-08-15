


from core.request.context import RequestContext


from ..config import DetailSpiderConfig
from ..context import SpiderContext

from ..typing import SpiderTemplate
from .base import SpiderStep, TemplateSpider

class TemplateDetailSpider(
    TemplateSpider[DetailSpiderConfig],
):

    template = SpiderTemplate.DETAIL



    async def process(
        self,
        context: SpiderContext[DetailSpiderConfig],
        request: RequestContext,
    ) -> SpiderStep:

        extract_context = (
            self._build_extract_context(
                request,
            )
        )

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