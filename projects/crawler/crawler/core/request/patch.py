from __future__ import annotations

from dataclasses import dataclass

from core.request.middleware.cookie.model import Cookie
from core.request.middleware.proxy.config import ProxyConfig

from .typing import (
    RequestBody,
    RequestParams,
    RequestHeaders,
)

_UNSET = object()

@dataclass(frozen=True, slots=True)
class RequestPatch:
    url: str | None = None
    headers: RequestHeaders | None = None
    cookies: tuple[Cookie, ...] = ()
    params: RequestParams | None = None
    body: RequestBody = _UNSET
    proxy: ProxyConfig | None = None
    def has_body(self) -> bool:
        return self.body is not _UNSET

