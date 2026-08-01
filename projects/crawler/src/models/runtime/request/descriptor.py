from dataclasses import dataclass, field
from typing import Any

from models.enums.http_method import HttpMethod
from models.enums.request_kind import RequestKind
from models.runtime.request.meta import RequestMeta
from models.runtime.request.profile import RequestProfile

@dataclass(slots=True,frozen=True)
class RequestDescriptor:

    url: str 

    method: HttpMethod | None = None

    kind: RequestKind | None = None

    profile: RequestProfile | None = None

    headers: dict[str, str] | None = None

    cookies: dict[str, str] | None = None

    params: dict[str, str] | None = None

    body: Any = None

    meta: RequestMeta = field(
        default_factory=RequestMeta,
    )