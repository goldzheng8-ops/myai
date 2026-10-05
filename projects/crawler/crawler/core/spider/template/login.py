from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import LoginSpiderConfig
from core.spider.template.base import RequestTemplate
class LoginRequestTemplate(
    RequestTemplate[LoginSpiderConfig],
):
    plugin_type = SpiderTemplate.LOGIN

    async def process(
        self,
        *,
        context: SpiderContext[LoginSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )