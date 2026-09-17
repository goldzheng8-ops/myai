from typing import Any

from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.request.downloader.factory import build_scrapy_downloader_factory, build_httpx_downloader_factory, build_playwright_downloader_factory
from core.request.downloader.manager import DownloaderManager
from core.request.typing import DownloaderType
from core.request.downloader.registry import DownloaderRegistry



def register_downloaders(
    builder: ProviderBuilder,
) -> None:
    
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
    
    builder.add_factory(
        DownloaderRegistry,
        lambda resolver: create_downloader_registry(
            resolver,
        ),
    )

def create_downloader_registry(
    resolver: ProviderResolver[Any, Any],
) -> DownloaderRegistry:

    registry = DownloaderRegistry()

    registry.register(
        DownloaderType.HTTPX,
        build_httpx_downloader_factory(
            resolver,
        ),
    )

    registry.register(
        DownloaderType.SCRAPY,
        build_scrapy_downloader_factory(
            resolver,
        ),
    )

    registry.register(
        DownloaderType.PLAYWRIGHT,
        build_playwright_downloader_factory(
            resolver,
        ),
    )

    return registry