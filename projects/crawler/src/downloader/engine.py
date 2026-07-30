
from downloader.registry import DownloaderRegistry
from core.result.download_result import DownloadResult
from core.context.request_context import RequestContext

class DownloaderEngine:

    def __init__(self,registry:DownloaderRegistry):

        self.registry = registry
        # self.pipeline = pipeline

    def download(self, request: RequestContext) -> DownloadResult:
        plugin = self.registry.create(request.profile.downloader)
        

        return plugin.download(request)