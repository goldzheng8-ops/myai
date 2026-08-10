from core.request.downloader.base import DownloaderPlugin
from core.request.typing import DownloaderType
from core.registry.base import Registry





class DownloaderRegistry(
    Registry[
        DownloaderType,
        DownloaderPlugin,
    ],
):
    pass


