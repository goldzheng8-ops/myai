from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

import httpx
from playwright.async_api import BrowserContext, Page
from scrapy.http import Response




@dataclass(frozen=True, slots=True, kw_only=True)
class RequestResponse:
    """
    Immutable transport-level response snapshot.

    Contains all response data required to reconstruct
    a ResponseAdapter after the original transport runtime
    has been released.

    This object is safe to store in response caches.
    """

    url: str
    status_code: int

    headers: Mapping[str, str] = field(
        default_factory=dict,
    )

    body: bytes = b""

    cookies: Mapping[str, str] = field(
        default_factory=dict,
    )

    encoding: str | None = None
    reason: str | None = None

    @property
    def text(self) -> str:
        encoding = self.encoding or "utf-8"

        return self.body.decode(
            encoding,
            errors="replace",
        )

@dataclass(frozen=True, slots=True)
class BrowserResponse(RequestResponse):
    """
    Browser-specific response produced by a browser downloader.
    """

    page: Page | None = None

    browser_context: BrowserContext | None = None

@dataclass(frozen=True, slots=True)
class HttpxResponse(RequestResponse):
    raw: httpx.Response | None = None


@dataclass(frozen=True, slots=True)
class ScrapyResponse(RequestResponse):
    raw: Response | None = None