from dataclasses import dataclass, field
from typing import Any

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor


@dataclass(slots=True)
class SpiderStep:
    request: RequestContext
    items: list[Any] = field(default_factory=list)
    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )
    continue_: bool = True