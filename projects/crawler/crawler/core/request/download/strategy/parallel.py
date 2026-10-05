import asyncio

from core.request.context import RequestContext
from core.request.download.chunk.downloader import ChunkDownloader
from core.request.download.chunk.model import ChunkPlan, ChunkRange
from core.request.download.chunk.planner import ChunkPlanner
from core.request.download.chunk.store import ChunkStore
from core.request.download.strategy.base import BaseChunkDownloadStrategy
from core.request.middleware.fingerprint.provider import FingerprintProvider


class ParallelDownloadStrategy(
    BaseChunkDownloadStrategy,
):

    def __init__(
        self,
        chunk_downloader: ChunkDownloader,
        chunk_planner: ChunkPlanner,
        chunk_store: ChunkStore,
        fingerprint_provider: FingerprintProvider,
        chunk_size: int,
        max_concurrency: int = 4,
    ) -> None:

        super().__init__(
            chunk_downloader=chunk_downloader,
            chunk_planner=chunk_planner,
            chunk_store=chunk_store,
            fingerprint_provider=fingerprint_provider,
            chunk_size=chunk_size,
        )

        if max_concurrency <= 0:
            raise ValueError(
                "max_concurrency must be greater "
                "than zero.",
            )

        self._max_concurrency = max_concurrency

    @property
    def strategy_name(self) -> str:
        return "parallel"

    async def _download_chunks(
        self,
        *,
        context: RequestContext,
        key: str,
        plan: ChunkPlan,
    ) -> None:

        semaphore = asyncio.Semaphore(
            self._max_concurrency,
        )

        async def download_one(
            chunk: ChunkRange,
        ) -> None:

            if await self._chunk_store.exists(
                key,
                chunk,
            ):
                return

            async with semaphore:

                response = (
                    await self._chunk_downloader.download(
                        context=context,
                        chunk=chunk,
                    )
                )

                try:
                    await self._chunk_store.write(
                        key,
                        chunk,
                        response.body,
                    )
                finally:
                    await response.close()

        await asyncio.gather(
            *(
                download_one(chunk)
                for chunk in plan.chunks
            )
        )