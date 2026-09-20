from __future__ import annotations

from abc import ABC
from typing import Generic

from core.request.context import RequestContext
from core.request.downloader.model import DownloaderCapabilities


from .plugin import DownloadResult, DownloaderPlugin
from .request import DownloadRequest

from .typing import ConfigT




class BaseDownloader(
    DownloaderPlugin,
    Generic[ConfigT],
    ABC,
):
    """
    Base implementation shared by concrete downloaders.
    """

    def __init__(
        self,
        config: ConfigT,
    ) -> None:

        self._config = config

    @property
    def capabilities(self) -> DownloaderCapabilities:
        return DownloaderCapabilities()
    @property
    def config(
        self,
    ) -> ConfigT:

        return self._config

    async def stream(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        raise NotImplementedError(
            f"{type(self).__name__} "
            "does not support streaming.",
        )

    def build_request(
        self,
        context: RequestContext,
    ) -> DownloadRequest:

        return DownloadRequest.from_context(
            context,
        )