from __future__ import annotations

from core.request.context import RequestContext

from core.spider.config import DownloadSpiderConfig
from core.spider.step import RequestStep
from core.spider.template.base import RequestTemplate

from ..context import SpiderContext

from core.output.model import DownloadBody, DownloadResult
from core.spider.typing import SpiderTemplate



class DownloadRequestTemplate(
    RequestTemplate[DownloadSpiderConfig],
):
    plugin_type = SpiderTemplate.DOWNLOAD

    async def process(
        self,
        *,
        context: SpiderContext[DownloadSpiderConfig],
        request: RequestContext,
    ) -> RequestStep:

        result = request.result

        if result is None:
            raise RuntimeError(
                "Download request produced no result.",
            )

        response = result.response

        download = DownloadResult(
            url=response.url,
            body=DownloadBody(body_bytes=response.body),
            content_type=response.headers.get(
                "content-type",
            ),
        )

        return RequestStep(
            request=request,
            download=download,
            outputs=context.config.outputs,
        )