from core.request.context import RequestContext
from core.request.download.factory import DownloadStrategyFactory
from core.request.downloader.manager import DownloaderManager
from core.request.result import RequestResult

from .base import RequestExecutor


class DownloaderRequestExecutor(
    RequestExecutor,
):
    """
    Executes requests through the configured downloader.
    """

    def __init__(
        self,
        manager: DownloaderManager,
        strategy_factory: DownloadStrategyFactory,
    ) -> None:
        self._manager = manager
        self._strategy_factory = (
            strategy_factory
        )

    @property
    def manager(
        self,
    ) -> DownloaderManager:
        return self._manager

    async def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:

        downloader_spec = context.config.profile.downloader
        print(downloader_spec.type)
        download_strategy = context.config.profile.download_strategy
        print(download_strategy)

        downloader = await self._manager.get(
            downloader_spec,
        )
        strategy = self._strategy_factory.create(
            strategy_type=download_strategy,
            downloader=downloader,
        )

        download_result = await strategy.download(
            context,
        )

        if download_result.response is None:
            if download_result.error is not None:
                raise download_result.error

            raise RuntimeError(
                "Downloader completed without a response.",
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