from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Literal

from core.request.downloader.typing import BrowserTypeName, WaitUntilState
from core.request.typing import DownloaderType
from core.typing.config import BaseConfig
from pydantic import Field

@dataclass(frozen=True, slots=True)
class DownloaderConfig:
    """
    Common configuration for downloader implementations.
    """

    timeout: float | None = None


@dataclass(frozen=True, slots=True)
class PlaywrightDownloaderConfig(
    DownloaderConfig,
):
    """
    Configuration for PlaywrightDownloader.
    """

    browser: BrowserTypeName  = "chromium"

    headless: bool = True

    wait_until: WaitUntilState  = "domcontentloaded"

    javascript: bool = True

    locale: str | None = None

    user_agent: str | None = None


@dataclass(frozen=True, slots=True)
class HttpxDownloaderConfig(
    DownloaderConfig,
):
    """
    Configuration for HTTPXDownloader.
    """

    verify_ssl: bool = True

    follow_redirects: bool = True

    max_redirects: int = 20

    http2: bool = False


@dataclass(frozen=True, slots=True)
class ScrapyDownloaderConfig(
    DownloaderConfig,
):
    """
    Configuration for ScrapyDownloader.
    """

    download_timeout: float | None = None


class HttpxDownloaderSpec(BaseConfig):
    type: Literal[DownloaderType.HTTPX] = DownloaderType.HTTPX
    config: HttpxDownloaderConfig

class PlaywrightDownloaderSpec(BaseConfig):
    type: Literal[DownloaderType.PLAYWRIGHT] = DownloaderType.PLAYWRIGHT
    config: PlaywrightDownloaderConfig

class ScrapyDownloaderSpec(BaseConfig):
    type: Literal[DownloaderType.SCRAPY] = DownloaderType.SCRAPY
    config: ScrapyDownloaderConfig

DownloaderSpecUnion = Annotated[
    (
        HttpxDownloaderSpec
        | PlaywrightDownloaderSpec
        | ScrapyDownloaderSpec
    ),
    Field(discriminator="type"),
]