from typing import Any

from core.request.downloader import BaseDownloader
from core.request.downloader.config import DownloaderSpecUnion
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
        spec: DownloaderSpecUnion
    ) -> BaseDownloader[Any]:
        downloader = self._instances.get(spec.type)

        if downloader is not None:
            return downloader

        downloader = self._registry.create_any(spec.type,spec.config)

        await self._lifecycle.acquire(downloader)

        self._instances[spec.type] = downloader

        return downloader