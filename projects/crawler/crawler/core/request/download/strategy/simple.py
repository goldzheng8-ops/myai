from typing import Any


from core.request.download.strategy.base import DownloadStrategy
from core.request.downloader.result import DownloadResult
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

        return await self._downloader.download(
            context,
        )

