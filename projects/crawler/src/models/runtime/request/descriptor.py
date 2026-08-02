from dataclasses import dataclass
from typing import Any

from models.enums.http_method import HttpMethod
from models.enums.request_kind import RequestKind
from models.runtime.request.meta import RequestMeta
from models.runtime.request.profile import RequestProfile

@dataclass(slots=True, frozen=True)
class RequestDescriptor:

    url: str

    kind: RequestKind

    profile: RequestProfile

    method: HttpMethod

    headers: dict[str, str]

    cookies: dict[str, str]

    params: dict[str, Any]

    body: Any

    meta: RequestMeta