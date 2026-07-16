from downloader.result import DownloadResult
from request import pipeline
from request.context import RequestContext
from downloader.registry import registry as downloader_registry

class DownloaderEngine:

    def __init__(self):

        self.registry = downloader_registry
        self.pipeline = pipeline

    def download(self, request: RequestContext) -> DownloadResult:
        plugin = self.registry.get(request.downloader)
        

        return plugin.download(request)