from typing import Any

from core.request.download.chunk.planner import ChunkPlanner
from core.request.download.chunk.store import ChunkStore
from core.request.download.exception import DownloadError
from core.request.download.range.parser import RangeParser
from core.request.download.resume.store import ResumeStore
from core.request.download.strategy.base import ChunkDownloader, DownloadStrategy
from core.request.download.strategy.chunked import ChunkedDownloadStrategy
from core.request.download.strategy.parallel import ParallelDownloadStrategy
from core.request.download.strategy.resumable import ResumableDownloadStrategy
from core.request.download.strategy.simple import SimpleDownloadStrategy
from core.request.download.strategy.streaming import StreamingDownloadStrategy
from core.request.download.typing import DownloadStrategyType
from core.request.downloader.base import BaseDownloader
from core.request.middleware.fingerprint.provider import FingerprintProvider

class DownloadStrategyFactory:

    def __init__(
        self,
        resume_store: ResumeStore,
        fingerprint_provider: FingerprintProvider,
        range_parser: RangeParser,
        chunk_planner: ChunkPlanner,
        chunk_store: ChunkStore,
        chunk_size: int,
        parallel_max_concurrency: int = 4,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero.",
            )

        if parallel_max_concurrency <= 0:
            raise ValueError(
                "parallel_max_concurrency must be "
                "greater than zero.",
            )

        self._resume_store = resume_store
        self._fingerprint_provider = (
            fingerprint_provider
        )
        self._range_parser = range_parser
        self._chunk_planner = chunk_planner
        self._chunk_store = chunk_store
        self._chunk_size = chunk_size

        self._parallel_max_concurrency = (
            parallel_max_concurrency
        )

    def create(
        self,
        strategy_type: DownloadStrategyType,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        match strategy_type:

            case DownloadStrategyType.SIMPLE:
                return self._create_simple(
                    downloader,
                )

            case DownloadStrategyType.RESUMABLE:
                return self._create_resumable(
                    downloader,
                )

            case DownloadStrategyType.CHUNKED:
                return self._create_chunked(
                    downloader,
                )

            case DownloadStrategyType.PARALLEL:
                return self._create_parallel(
                    downloader,
                )

            case DownloadStrategyType.STREAMING:
                return self._create_streaming(
                    downloader,
                )

            case _:
                raise DownloadError(
                    f"Unsupported download strategy: "
                    f"{strategy_type!r}",
                )

    def _create_simple(
        self,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        return SimpleDownloadStrategy(
            downloader=downloader,
        )

    def _create_resumable(
        self,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        if not downloader.capabilities.supports_resumable:
            raise DownloadError(
                f"Downloader "
                f"{type(downloader).__name__!r} "
                "does not support resumable downloads.",
            )

        return ResumableDownloadStrategy(
            downloader=downloader,
            resume_store=self._resume_store,
            fingerprint_provider=(
                self._fingerprint_provider
            ),
            range_parser=self._range_parser,
        )

    def _create_chunked(
        self,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        if not downloader.capabilities.supports_range:
            raise DownloadError(
                f"Downloader "
                f"{type(downloader).__name__!r} "
                "does not support range downloads.",
            )

        chunk_downloader = ChunkDownloader(
            downloader=downloader,
            range_parser=self._range_parser,
        )

        return ChunkedDownloadStrategy(
            chunk_downloader=chunk_downloader,
            chunk_planner=self._chunk_planner,
            chunk_store=self._chunk_store,
            fingerprint_provider=(
                self._fingerprint_provider
            ),
            chunk_size=self._chunk_size,
        )

    def _create_parallel(
        self,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        if not downloader.capabilities.supports_range:
            raise DownloadError(
                f"Downloader "
                f"{type(downloader).__name__!r} "
                "does not support range downloads.",
            )

        chunk_downloader = ChunkDownloader(
            downloader=downloader,
            range_parser=self._range_parser,
        )

        return ParallelDownloadStrategy(
            chunk_downloader=chunk_downloader,
            chunk_planner=self._chunk_planner,
            chunk_store=self._chunk_store,
            fingerprint_provider=(
                self._fingerprint_provider
            ),
            chunk_size=self._chunk_size,
            max_concurrency=(
                self._parallel_max_concurrency
            ),
        )

    def _create_streaming(
        self,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        if not downloader.capabilities.supports_streaming:
            raise DownloadError(
                f"Downloader "
                f"{type(downloader).__name__!r} "
                "does not support streaming downloads.",
            )

        return StreamingDownloadStrategy(
            downloader=downloader,
        )