from abc import ABC, abstractmethod

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

    def __init__(
        self,
        chunk_downloader: ChunkDownloader,
        chunk_planner: ChunkPlanner,
        chunk_store: ChunkStore,
        fingerprint_provider: FingerprintProvider,
        chunk_size: int,
    ) -> None:

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

        key = (
            self._fingerprint_provider.fingerprint(
                context.descriptor,
            )
        )

        probe_response, probe_range, ranges_supported = (
            await self._chunk_downloader.probe(
                context=context,
            )
        )

        try:

            # If ranges are not supported, return the full probe
            # response body as the downloaded content.
            if not ranges_supported:

                # The probe_response already contains the full body.
                response = probe_response

                return DownloadResult(
                    response=response,
                    success=True,
                    meta={
                        "download_strategy": self.strategy_name,
                        "chunk_count": 1,
                        "total_size": probe_range.total,
                        "ranges_supported": False,
                    },
                )

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

                response = probe_response.with_body(
                    body,
                )

                await probe_response.close()

                return DownloadResult(
                    response=response,
                    success=True,
                    meta={
                        "download_strategy": self.strategy_name,
                        "chunk_count": plan.count,
                        "total_size": plan.total_size,
                    },
                )

            except DownloadError:
                # If chunked download fails (for example server
                # returns 206 but chunk responses lack Content-Range),
                # fall back to a single full GET.
                try:
                    full_response = await self._chunk_downloader.fetch_full(
                        context=context,
                    )

                    return DownloadResult(
                        response=full_response,
                        success=True,
                        meta={
                            "download_strategy": self.strategy_name,
                            "chunk_count": 1,
                            "total_size": total_size,
                            "ranges_supported": False,
                        },
                    )

                finally:
                    await self._chunk_store.delete(key)

        except Exception:
            await probe_response.close()
            raise

        finally:
            await self._chunk_store.delete(key)

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

            if len(body) != chunk.size:
                raise DownloadIncompleteError(
                    url=url,
                    downloaded=total + len(body),
                    expected=plan.total_size,
                )

            parts.append(body)

            total += len(body)

        if total != plan.total_size:
            raise DownloadIncompleteError(
                url=url,
                downloaded=total,
                expected=plan.total_size,
            )

        return b"".join(parts)