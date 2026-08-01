
from downloader.registry import DownloaderRegistry
from models.runtime.download_result import DownloadResult
from models.runtime.request_context import RequestContext

class DownloaderEngine:

    def __init__(self,registry:DownloaderRegistry):

        self.registry = registry
        # self.pipeline = pipeline

    def download(self, request: RequestContext) -> DownloadResult:
        plugin = self.registry.create(request.profile.downloader)
        

        return plugin.download(request)