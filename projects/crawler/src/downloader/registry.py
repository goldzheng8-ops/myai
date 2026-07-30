from downloader.base import DownloaderPlugin
from enums.downloader_type import DownloaderType
from core.registry.factory import FactoryPluginRegistry





class DownloaderRegistry(
    FactoryPluginRegistry[
        DownloaderType,
        DownloaderPlugin,
    ],
):
    pass


