from abc import ABC, abstractmethod

from core.extraction.response.base import ResponseAdapter
from core.request.download.range.model import ByteRange
from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext
from core.request.download.chunk.downloader import ChunkDownloader
from core.request.download.chunk.model import ChunkPlan
from core.request.download.chunk.planner import ChunkPlanner
from core.request.download.chunk.store import ChunkStore
from core.request.download.exception import DownloadError, DownloadIncompleteError
from core.request.middleware.fingerprint.provider import FingerprintProvider

class DownloadStrategy(ABC):

    @abstractmethod
    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        raise NotImplementedError

class BaseChunkDownloadStrategy(
    DownloadStrategy,
    ABC,
):
    """
    Base implementation for range-based chunk downloads.

    The base class owns the complete lifecycle:

        probe
          ↓
        determine range support
          ↓
        build ChunkPlan
          ↓
        download chunks
          ↓
        assemble chunks
          ↓
        build final response

    Subclasses only decide how chunks are downloaded.
    """

    def __init__(
        self,
        chunk_downloader: ChunkDownloader,
        chunk_planner: ChunkPlanner,
        chunk_store: ChunkStore,
        fingerprint_provider: FingerprintProvider,
        chunk_size: int,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero.",
            )

        self._chunk_downloader = chunk_downloader
        self._chunk_planner = chunk_planner
        self._chunk_store = chunk_store
        self._fingerprint_provider = (
            fingerprint_provider
        )
        self._chunk_size = chunk_size

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        key = self._fingerprint_provider.fingerprint(
            context.descriptor,
        )

        probe_response, probe_range, ranges_supported = (
            await self._chunk_downloader.probe(
                context=context,
            )
        )

        try:
            if not ranges_supported:
                return await self._handle_non_range_response(
                    response=probe_response,
                    byte_range=probe_range,
                )

            return await self._download_range_based(
                context=context,
                key=key,
                probe_response=probe_response,
                probe_range=probe_range,
            )

        finally:
            await self._chunk_store.delete(key)

    async def _handle_non_range_response(
        self,
        *,
        response: ResponseAdapter,
        byte_range: ByteRange,
    ) -> DownloadResult:

        return DownloadResult(
            response=response,
            success=True,
            meta={
                "download_strategy": self.strategy_name,
                "chunk_count": 1,
                "total_size": byte_range.total,
                "ranges_supported": False,
            },
        )

    async def _download_range_based(
        self,
        *,
        context: RequestContext,
        key: str,
        probe_response: ResponseAdapter,
        probe_range: ByteRange,
    ) -> DownloadResult:

        total_size = probe_range.total

        if total_size is None:
            raise DownloadError(
                "Content-Range does not contain "
                "a known total size.",
                url=context.descriptor.url,
            )

        plan = self._chunk_planner.plan(
            total_size=total_size,
            chunk_size=self._chunk_size,
        )

        try:
            await self._download_chunks(
                context=context,
                key=key,
                plan=plan,
            )

            body = await self._assemble(
                url=context.descriptor.url,
                key=key,
                plan=plan,
            )

            return self._build_result(
                response=probe_response,
                body=body,
                plan=plan,
            )

        except DownloadError:
            return await self._fallback_to_full_download(
                context=context,
                probe_response=probe_response,
                total_size=total_size,
            )

    async def _fallback_to_full_download(
        self,
        *,
        context: RequestContext,
        probe_response: ResponseAdapter,
        total_size: int,
    ) -> DownloadResult:

        await probe_response.close()

        full_response = await (
            self._chunk_downloader.fetch_full(
                context=context,
            )
        )

        return DownloadResult(
            response=full_response,
            success=True,
            meta={
                "download_strategy": self.strategy_name,
                "chunk_count": 1,
                "total_size": total_size,
                "ranges_supported": False,
                "fallback": True,
            },
        )

    def _build_result(
        self,
        *,
        response: ResponseAdapter,
        body: bytes,
        plan: ChunkPlan,
    ) -> DownloadResult:

        complete_response = response.with_body(
            body,
        )

        return DownloadResult(
            response=complete_response,
            success=True,
            meta={
                "download_strategy": self.strategy_name,
                "chunk_count": plan.count,
                "total_size": plan.total_size,
                "ranges_supported": True,
            },
        )

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        ...

    @abstractmethod
    async def _download_chunks(
        self,
        *,
        context: RequestContext,
        key: str,
        plan: ChunkPlan,
    ) -> None:
        ...

    async def _assemble(
        self,
        *,
        url: str,
        key: str,
        plan: ChunkPlan,
    ) -> bytes:

        parts: list[bytes] = []

        total = 0

        for chunk in plan.chunks:

            body = await self._chunk_store.read(
                key,
                chunk,
            )

            actual_size = len(body)

            if actual_size != chunk.size:
                raise DownloadIncompleteError(
                    url=url,
                    downloaded=total + actual_size,
                    expected=plan.total_size,
                )

            parts.append(body)

            total += actual_size

        if total != plan.total_size:
            raise DownloadIncompleteError(
                url=url,
                downloaded=total,
                expected=plan.total_size,
            )

        return b"".join(parts)