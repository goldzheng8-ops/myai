from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from enums.downloader_type import DownloaderType
from runtime.download_result import DownloadResult
from runtime.request_context import RequestContext



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