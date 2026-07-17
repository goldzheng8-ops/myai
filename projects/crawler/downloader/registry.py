

from downloader.base import DownloaderPlugin
from downloader.plugins.playwright import PlaywrightDownloader
from downloader.plugins.requests import RequestsDownloader



class DownloaderRegistry:

    def __init__(self):
        self._plugins = dict[str, DownloaderPlugin]()

    def register(self, name: str, plugin: DownloaderPlugin):
        self._plugins[name] = plugin

    def get(self, name: str) -> DownloaderPlugin:
        return self._plugins[name]
    

registry = DownloaderRegistry()

registry.register("requests", RequestsDownloader())
registry.register("playwright", PlaywrightDownloader())
