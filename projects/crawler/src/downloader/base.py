from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from enums.downloader_type import DownloaderType
from core.plugin.base import Plugin
from core.result.download_result import DownloadResult
from core.context.request_context import RequestContext



class DownloaderPlugin(Plugin,ABC):
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