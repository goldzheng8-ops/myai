from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

import httpx
from playwright.async_api import BrowserContext, Page
from scrapy.http import Response




@dataclass(frozen=True, slots=True,kw_only= True)
class RequestResponse:
    """
    Raw response produced by request execution.

    This model belongs to the request layer and contains
    only transport-level response data.
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


@dataclass(frozen=True, slots=True)
class BrowserResponse(RequestResponse):
    """
    Browser-specific response produced by a browser downloader.
    """

    page: Page | None = None

    browser_context: BrowserContext | None = None

@dataclass(frozen=True, slots=True)
class HttpxResponse(RequestResponse):
    """
    HTTPX-specific response produced by HTTPX downloader.
    """

    raw: httpx.Response

@dataclass(frozen=True, slots=True)
class ScrapyResponse(RequestResponse):
    """
    Scrapy-specific response produced by Scrapy downloader.
    """

    raw: Response
