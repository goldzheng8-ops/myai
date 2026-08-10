from __future__ import annotations

from dataclasses import dataclass, field

from core.request.middleware.proxy.model import ProxyConfig

from .meta import RequestMeta
from .profile import RequestProfile
from .typing import (
    HttpMethod,
    RequestBody,
    RequestCookies,
    RequestHeaders,
    RequestParams,
    RequestKind,
)


@dataclass(frozen=True, slots=True)
class RequestDescriptor:

    url: str

    kind: RequestKind

    profile: RequestProfile

    method: HttpMethod = HttpMethod.GET

    headers: RequestHeaders = field(
        default_factory=dict,
    )

    cookies: RequestCookies = field(
        default_factory=dict,
    )

    params: RequestParams = field(
        default_factory=dict,
    )

    body: RequestBody = None

    proxy: ProxyConfig | None = None

    meta: RequestMeta = field(
        default_factory=RequestMeta,
    )