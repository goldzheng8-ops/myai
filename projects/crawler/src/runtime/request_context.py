from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.request import RequestConfig
from enums.request_kind import RequestKind
from runtime.request_profile import RequestProfile
from runtime.spider_context import SpiderContext

@dataclass(slots=True)
class RequestContext:

    spider: SpiderContext

    request: RequestConfig

    kind: RequestKind

    profile: RequestProfile

    meta: dict[str, Any] = field(default_factory=dict)