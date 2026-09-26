from __future__ import annotations

from dataclasses import dataclass, field

from core.request.middleware.cookie.model import Cookie
from core.request.middleware.proxy.config import ProxyConfig

from .meta import RequestMeta
from .profile import RequestProfile
from .typing import (
    HttpMethod,
    RequestBody,
    RequestHeaders,
    RequestParams,
    RequestKind,
)


@dataclass(frozen=True, slots=True)
class RequestDescriptor:

    url: str

    kind: RequestKind

    profile: RequestProfile

    target_spider: str 

    method: HttpMethod = HttpMethod.GET

    headers: RequestHeaders = field(
        default_factory=dict,
    )

    cookies: tuple[Cookie, ...] = ()

    params: RequestParams = field(
        default_factory=dict,
    )

    body: RequestBody = None

    proxy: ProxyConfig | None = None

    meta: RequestMeta = field(
        default_factory=RequestMeta,
    )