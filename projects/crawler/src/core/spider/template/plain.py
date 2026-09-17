from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import PlainSpiderConfig
from core.spider.template.base import RequestTemplate


class PlainRequestTemplate(
    RequestTemplate[PlainSpiderConfig],
):
    plugin_type = SpiderTemplate.PLAIN

    async def process(
        self,
        *,
        context: SpiderContext[PlainSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )