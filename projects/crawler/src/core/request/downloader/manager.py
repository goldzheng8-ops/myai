from typing import Any

from core.request.downloader import BaseDownloader
from core.request.downloader.config import DownloaderConfig
from core.request.downloader.registry import DownloaderRegistry
from core.lifecycle.manager import LifecycleManager
from core.request.typing import DownloaderType

class DownloaderManager:
    def __init__(
        self,
        registry: DownloaderRegistry,
        lifecycle: LifecycleManager,
    ) -> None:
        self._registry = registry
        self._lifecycle = lifecycle
        self._instances: dict[
            DownloaderType,
            BaseDownloader[Any],
        ] = {}

    async def get(
        self,
        type_: DownloaderType,
        config: DownloaderConfig | None = None,        
    ) -> BaseDownloader[Any]:
        downloader = self._instances.get(type_)

        if downloader is not None:
            return downloader

        downloader = self._registry.create_any(type_,config)

        await self._lifecycle.acquire(downloader)

        self._instances[type_] = downloader

        return downloader