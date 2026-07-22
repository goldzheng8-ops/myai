from dataclasses import dataclass, field
from typing import Any

from enums.discovery_type import DiscoveryType
from enums.http_method import HttpMethod
from enums.request_kind import RequestKind
from runtime.request_profile import RequestProfile

@dataclass(slots=True)
class RequestDelta:

    url: str

    discovery: DiscoveryType

    kind: RequestKind

    profile: RequestProfile

    method: HttpMethod = HttpMethod.GET

    headers: dict[str, str] = field(default_factory=dict)

    params: dict[str, str] = field(default_factory=dict)

    body: Any = None

    priority: int = 0

    meta: dict[str, Any] = field(default_factory=dict)