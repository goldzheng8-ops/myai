from __future__ import annotations
from typing import Any, Literal, overload
from core.registry import Registry
from core.request.downloader.base import BaseDownloader
from core.request.downloader.factory import DownloaderFactory
from core.request.downloader.httpx import HttpxDownloader
from core.request.downloader.playwright import PlaywrightDownloader
from core.request.downloader.scrapy.downloader import ScrapyDownloader
from core.request.downloader.config import HttpxDownloaderConfig, PlaywrightDownloaderConfig, ScrapyDownloaderConfig
from core.request.typing import DownloaderType
from .config import DownloaderConfig

DownloaderFactoryAny = DownloaderFactory[Any]

class DownloaderRegistry(
    Registry[
        DownloaderType,
        DownloaderFactoryAny,
    ],
):

    @overload
    def create(
        self,
        type_: Literal[DownloaderType.HTTPX],
        config: HttpxDownloaderConfig | None = None,
    ) -> HttpxDownloader:
        ...

    @overload
    def create(
        self,
        type_: Literal[DownloaderType.SCRAPY],
        config: ScrapyDownloaderConfig | None = None,
    ) -> ScrapyDownloader:
        ...

    @overload
    def create(
        self,
        type_: Literal[DownloaderType.PLAYWRIGHT],
        config: PlaywrightDownloaderConfig | None = None,
    ) -> PlaywrightDownloader:
        ...

    def create(
        self,
        type_: DownloaderType,
        config: DownloaderConfig | None = None,
    ) -> BaseDownloader[Any]:
        return self._create(
            type_,
            config,
        )
    def create_any(
        self,
        type_: DownloaderType,
        config: DownloaderConfig | None = None,
    ) -> BaseDownloader[Any]:
        return self._create(type_, config)
    def _create(
        self,
        type_: DownloaderType,
        config: Any = None,
    ) -> BaseDownloader[Any]:
        factory = self.get(type_)
        return factory(config)