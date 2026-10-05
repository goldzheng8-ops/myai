from __future__ import annotations
from typing import Literal, TypeVar, TYPE_CHECKING


if TYPE_CHECKING:

    from core.request.downloader.config import DownloaderConfig




ConfigT = TypeVar(
    "ConfigT",
    bound="DownloaderConfig",
)


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