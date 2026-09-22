from typing import Any

from application.config.model import ApplicationConfig
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder, ProviderResolver
from core.request.downloader.aria2.client import Aria2Client
from core.request.downloader.aria2.monitor import Aria2DownloadMonitor
from core.request.downloader.aria2.options import Aria2OptionsBuilder
from core.request.downloader.factory import build_aria2_downloader_factory, build_scrapy_downloader_factory, build_httpx_downloader_factory, build_playwright_downloader_factory
from core.request.downloader.manager import DownloaderManager
from core.request.typing import DownloaderType
from core.request.downloader.registry import DownloaderRegistry



def register_downloaders(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        Aria2Client,
        lambda resolver: Aria2Client(
            rpc_url=config.aria2.rpc_url,
            rpc_secret=config.aria2.rpc_secret,
            timeout=config.aria2.rpc_timeout,
        ),
    )

    builder.add_factory(
        Aria2DownloadMonitor,
        lambda resolver: Aria2DownloadMonitor(
            client=resolver.resolve(
                Aria2Client,
            ),
            poll_interval=config.aria2.poll_interval,
            timeout=config.aria2.monitor_timeout,
        ),
    )

    builder.add_factory(
        Aria2OptionsBuilder,
        lambda resolver: Aria2OptionsBuilder(
            directory=config.aria2.download_directory,
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
    registry.register(
        DownloaderType.ARIA2,
        build_aria2_downloader_factory(
            resolver,
        ),
    )

    return registry