from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RequestContext:

    downloader: str = "requests"

    url: str

    method: str = "GET"

    headers: dict[str, str] = field(default_factory=dict)

    cookies: dict[str, str] = field(default_factory=dict)

    params: dict[str, Any] = field(default_factory=dict)

    body: Any = None

    timeout: int = 30

    meta: dict[str, Any] = field(default_factory=dict)

    retry: int = 0

    priority: int = 0

    proxy: str | None = None