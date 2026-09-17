
from typing import Any, Protocol

from core.extraction.response.resolver import ResponseAdapterResolver
from core.provider import ProviderResolver
from core.request.downloader.config import HttpxDownloaderConfig, PlaywrightDownloaderConfig, ScrapyDownloaderConfig
from core.request.downloader.httpx import HttpxDownloader
from core.request.downloader.playwright import PlaywrightDownloader
from core.request.downloader.scrapy.bridge import ScrapyRequestBridge
from core.request.downloader.scrapy.downloader import ScrapyDownloader
from core.request.downloader.scrapy.executor import ScrapyRequestExecutor
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

def build_scrapy_downloader_factory(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderFactory[ScrapyDownloaderConfig]:

    def factory(
        config: ScrapyDownloaderConfig | None = None,
    ) -> ScrapyDownloader:
        return ScrapyDownloader(
            executor=resolver.resolve(
                ScrapyRequestExecutor,
            ),
            bridge=resolver.resolve(
                ScrapyRequestBridge,
            ),
            response_adapter_resolver=resolver.resolve(
                ResponseAdapterResolver,
            ),
            config=config,
        )
    
    return factory

def build_httpx_downloader_factory(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderFactory[HttpxDownloaderConfig]:

    def factory(
        config: HttpxDownloaderConfig | None = None,
    ) -> HttpxDownloader:
        return HttpxDownloader(
            response_adapter_resolver=resolver.resolve(
                ResponseAdapterResolver,
            ),
            config=config,
        )
    
    return factory

def build_playwright_downloader_factory(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderFactory[PlaywrightDownloaderConfig]:

    def factory(
        config: PlaywrightDownloaderConfig | None = None,
    ) -> PlaywrightDownloader:
        return PlaywrightDownloader(
            response_adapter_resolver=resolver.resolve(
                ResponseAdapterResolver,
            ),
            config=config,
        )

    return factory