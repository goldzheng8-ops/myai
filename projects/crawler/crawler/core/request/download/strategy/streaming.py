from typing import Any

from core.request.context import RequestContext
from core.request.download.exception import DownloadError
from core.request.download.strategy.base import DownloadStrategy
from core.request.downloader.base import BaseDownloader
from core.request.downloader.result import DownloadResult

class StreamingDownloadStrategy(
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

        if not self._downloader.capabilities.supports_streaming:
            return DownloadResult(
                success=False,
                error=DownloadError(
                    "Downloader does not support streaming.",
                    url=context.descriptor.url,
                ),
            )

        result = await self._downloader.stream(
            context,
        )

        return result