from __future__ import annotations
from typing import Literal
from collections.abc import Awaitable, Callable

from core.request.context import RequestContext

from .request import DownloadRequest
from .result import DownloadResult


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