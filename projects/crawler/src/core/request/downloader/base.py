from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from core.request.context import RequestContext

from .config import DownloaderConfig
from .plugin import DownloaderPlugin
from .request import DownloadRequest


ConfigT = TypeVar(
    "ConfigT",
    bound=DownloaderConfig,
)


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
    def config(
        self,
    ) -> ConfigT:

        return self._config

    async def start(
        self,
    ) -> None:

        return None

    async def close(
        self,
    ) -> None:

        return None

    def build_request(
        self,
        context: RequestContext,
    ) -> DownloadRequest:

        return DownloadRequest.from_context(
            context,
        )