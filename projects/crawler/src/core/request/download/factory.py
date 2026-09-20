from typing import Any

from core.request.download.exception import DownloadError
from core.request.download.resume.base import ResumeStore
from core.request.download.strategy.base import DownloadStrategy
from core.request.download.strategy.resumable import ResumableDownloadStrategy
from core.request.download.strategy.simple import SimpleDownloadStrategy
from core.request.download.typing import DownloadStrategyType
from core.request.downloader.base import BaseDownloader
from core.request.middleware.fingerprint.provider import FingerprintProvider

class DownloadStrategyFactory:

    def __init__(
        self,
        resume_store: ResumeStore,
        fingerprint_provider: FingerprintProvider,
    ) -> None:

        self._resume_store = resume_store
        self._fingerprint_provider = (
            fingerprint_provider
        )

    def create(
        self,
        strategy_type: DownloadStrategyType,
        downloader: BaseDownloader[Any],
    ) -> DownloadStrategy:

        match strategy_type:

            case DownloadStrategyType.SIMPLE:
                return SimpleDownloadStrategy(
                    downloader=downloader,
                )

            case DownloadStrategyType.RESUMABLE:

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
                )

            case _:
                raise DownloadError(
                    f"Unsupported download strategy: "
                    f"{strategy_type!r}",
                )