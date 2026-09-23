from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import FormSpiderConfig
from core.spider.template.base import RequestTemplate
class FormRequestTemplate(
    RequestTemplate[FormSpiderConfig],
):
    plugin_type = SpiderTemplate.FORM

    async def process(
        self,
        *,
        context: SpiderContext[FormSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )