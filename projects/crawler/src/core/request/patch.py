from __future__ import annotations

from dataclasses import dataclass

from core.request.middleware.proxy.model import ProxyConfig

from .typing import (
    RequestBody,
    RequestParams,
    RequestCookies,
    RequestHeaders,
)

_UNSET = object()

@dataclass(frozen=True, slots=True)
class RequestPatch:
    url: str | None = None
    headers: RequestHeaders | None = None
    cookies: RequestCookies | None = None
    params: RequestParams | None = None
    body: RequestBody = _UNSET
    proxy: ProxyConfig | None = None
    def has_body(self) -> bool:
        return self.body is not _UNSET

