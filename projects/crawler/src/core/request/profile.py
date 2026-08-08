from __future__ import annotations

from dataclasses import dataclass

from .typing import(
    DownloaderType,
    ResponseFormat,
)


@dataclass(frozen=True, slots=True)
class RequestProfile:
    """
    Execution profile of a request.
    """

    downloader: DownloaderType

    response_format: ResponseFormat