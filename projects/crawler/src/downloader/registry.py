

from downloader.base import DownloaderPlugin
from downloader.config.enums import DownloaderType




class DownloaderRegistry:

    def __init__(self):
        self._plugins = dict[DownloaderType, DownloaderPlugin]()

    def register(self, plugin: DownloaderPlugin):
        self._plugins[plugin.type] = plugin

    def get(self, type: DownloaderType) -> DownloaderPlugin:
        return self._plugins[type]
    


