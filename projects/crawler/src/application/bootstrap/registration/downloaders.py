from typing import Any

from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.request.downloader.factory import build_scrapy_downloader_factory, create_httpx_downloader, create_playwright_downloader
from core.request.downloader.manager import DownloaderManager
from core.request.typing import DownloaderType
from core.request.downloader.registry import DownloaderRegistry



def register_downloaders(
    builder: ProviderBuilder,
) -> None:
    builder.add_factory(
        DownloaderRegistry,
        lambda resolver: create_downloader_registry(
            resolver,
        ),
    )
    builder.add_factory(
        DownloaderManager,
        lambda resolver: DownloaderManager(
            registry=resolver.resolve(
                DownloaderRegistry,
            ),
            lifecycle=resolver.resolve(
                LifecycleManager,
            ),
        ),
    )

def create_downloader_registry(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderRegistry:

    registry = DownloaderRegistry()

    registry.register(
        DownloaderType.HTTPX,
        create_httpx_downloader,
    )

    registry.register(
        DownloaderType.SCRAPY,
        build_scrapy_downloader_factory(
            resolver,
        ),
    )

    registry.register(
        DownloaderType.PLAYWRIGHT,
        create_playwright_downloader,
    )

    return registry