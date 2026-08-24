from __future__ import annotations
from typing import Literal, TypeVar
from collections.abc import Awaitable, Callable

from core.request.context import RequestContext
from core.request.downloader.config import DownloaderConfig

from .request import DownloadRequest
from .result import DownloadResult


ConfigT = TypeVar(
    "ConfigT",
    bound=DownloaderConfig,
)

DownloadHandler = Callable[
    [RequestContext],
    Awaitable[DownloadResult],
]


DownloadRequestBuilder = Callable[
    [RequestContext],
    DownloadRequest,
]


DownloadResultHandler = Callable[
    [RequestContext],
    Awaitable[DownloadResult],
]

WaitUntilState = Literal[
    "commit",
    "domcontentloaded",
    "load",
    "networkidle",
]

BrowserTypeName = Literal[
    "chromium",
    "firefox",
    "webkit",
]