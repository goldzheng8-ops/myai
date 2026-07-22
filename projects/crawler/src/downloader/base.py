from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from downloader.config.enums import DownloaderType
from downloader.result import DownloadResult
from request.context import RequestContext


class DownloaderPlugin(ABC):
    type:ClassVar[DownloaderType]

    @abstractmethod
    async def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:
        """
        根据 RequestContext 下载页面，返回统一的 DownloadResult。
        """
        raise NotImplementedError