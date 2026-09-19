from typing import Any

from core.download.exception import DownloadError
from core.download.strategy.base import DownloadStrategy
from core.output.model import DownloadResult,DownloadBody
from core.request.context import RequestContext
from core.request.downloader.base import BaseDownloader


class SimpleDownloadStrategy(
    DownloadStrategy,
):

    def __init__(
        self,
        downloader: BaseDownloader[Any],
    ) -> None:
        self._downloader = downloader

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        result = await self._downloader.download(
            context,
        )

        if not result.success:
            raise DownloadError(
                "Download failed.",
                url=context.descriptor.url,
                cause=result.error,
            )
        response = result.response
        if response is None:
            raise RuntimeError(
                "response should be  "
                "ResponseAdapter .",
            )
        return DownloadResult(
            url=response.url,
            body=DownloadBody(body_bytes=response.body),

            content_type=response.headers.get(
                "content-type",
            ),
            filename=None,
            headers=response.headers,
            size=len(response.body),
            metadata=result.meta,
        )