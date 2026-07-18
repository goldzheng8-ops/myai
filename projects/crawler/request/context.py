from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.config import CrawlerConfig, RequestConfig


@dataclass(slots=True)
class RequestContext:


    request: RequestConfig

    crawler: CrawlerConfig

    meta: dict[str, Any] = field(default_factory=dict)

    downloader: str = "requests"


