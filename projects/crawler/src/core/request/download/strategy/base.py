from abc import ABC, abstractmethod

from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext


class DownloadStrategy(ABC):

    @abstractmethod
    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        raise NotImplementedError