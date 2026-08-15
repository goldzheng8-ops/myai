from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from core.plugin import Plugin
from core.request.context import RequestContext
from core.request.typing import DownloaderType

from .result import DownloadResult


class DownloaderPlugin(
    Plugin,
    ABC,
):
    """
    Public contract implemented by all request downloaders.
    """

    type: ClassVar[DownloaderType]

    @abstractmethod
    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        """
        Execute the request represented by the context.
        """

        raise NotImplementedError