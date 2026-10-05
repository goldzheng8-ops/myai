from core.spider.typing import SpiderTemplate
from core.request.context import RequestContext
from core.spider.context import SpiderContext
from core.spider.step import RequestStep
from core.spider.config import UploadSpiderConfig
from core.spider.template.base import RequestTemplate
class UploadRequestTemplate(
    RequestTemplate[UploadSpiderConfig],
):
    plugin_type = SpiderTemplate.UPLOAD

    async def process(
        self,
        *,
        context: SpiderContext[UploadSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        return RequestStep(
            request=request,
            outputs=context.config.outputs,
        )