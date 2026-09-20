from core.request.context import RequestContext
from core.request.download.chunk.model import ChunkPlan
from core.request.download.strategy.base import BaseChunkDownloadStrategy


class ChunkedDownloadStrategy(
    BaseChunkDownloadStrategy,
):

    @property
    def strategy_name(self) -> str:
        return "chunked"

    async def _download_chunks(
        self,
        *,
        context: RequestContext,
        key: str,
        plan: ChunkPlan,
    ) -> None:

        for chunk in plan.chunks:

            if await self._chunk_store.exists(
                key,
                chunk,
            ):
                continue

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