from __future__ import annotations

from dataclasses import dataclass

from core.request.downloader.config import DownloaderSpecUnion

from .typing import(
    ResponseFormat,
)


@dataclass(frozen=True, slots=True)
class RequestProfile:
    """
    Execution profile of a request.
    """

    downloader: DownloaderSpecUnion

    response_format: ResponseFormat