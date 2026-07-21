from __future__ import annotations

from abc import ABC, abstractmethod

from downloader.result import DownloadResult
from request.context import RequestContext


class DownloaderPlugin(ABC):

    @abstractmethod
    async def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:
        """
        根据 RequestContext 下载页面，返回统一的 DownloadResult。
        """
        raise NotImplementedError