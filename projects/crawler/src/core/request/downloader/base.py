from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from core.request.typing import DownloaderType
from core.plugin.base import Plugin
from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext



class DownloaderPlugin(Plugin,ABC):
    type:ClassVar[DownloaderType]

    @abstractmethod
    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        """
        根据 RequestContext 下载页面，返回统一的 DownloadResult。
        """
        raise NotImplementedError