from core.request.context import RequestContext
from core.request.result import RequestResult

from core.request.downloader import (
    DownloaderRegistry,
)

from .base import RequestExecutor


class DownloaderRequestExecutor(
    RequestExecutor,
):
    """
    Executes requests through the configured downloader.
    """

    def __init__(
        self,
        registry: DownloaderRegistry,
    ) -> None:

        self._registry = registry

    @property
    def registry(
        self,
    ) -> DownloaderRegistry:

        return self._registry

    async def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:

        downloader_type = (
            context.descriptor.profile.downloader
        )

        downloader = self._registry.get(
            downloader_type,
        )

        download_result = await downloader.download(
            context,
        )

        context.result = RequestResult(
            response=download_result.response,
            success=download_result.success,
            error=download_result.error,
            elapsed=download_result.elapsed,
            meta=dict(download_result.meta),
            trace=list(download_result.trace),
        )

        return context