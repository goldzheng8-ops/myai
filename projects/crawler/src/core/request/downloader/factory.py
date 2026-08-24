
from typing import Protocol

from core.request.downloader.typing import ConfigT

from .base import BaseDownloader

class DownloaderFactory(
    Protocol[ConfigT],
):
    def __call__(
        self,
        config: ConfigT | None = None,
    ) -> BaseDownloader[ConfigT]:
        ...