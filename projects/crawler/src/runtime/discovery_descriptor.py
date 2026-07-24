from dataclasses import dataclass
from typing import Any

from enums.http_method import HttpMethod
from enums.request_kind import RequestKind
from runtime.request_profile import RequestProfile

@dataclass(slots=True)
class RequestDescriptor:

    url: str |None = None

    method: HttpMethod | None = None

    headers: dict[str, str] | None = None

    cookies: dict[str, str] | None = None

    params: dict[str, str] | None = None

    body: Any = None

    kind: RequestKind | None = None

    profile: RequestProfile | None = None

    meta: dict[str, Any] | None = None