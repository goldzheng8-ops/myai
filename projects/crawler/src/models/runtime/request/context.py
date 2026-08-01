from __future__ import annotations

from dataclasses import dataclass, field



from models.runtime.request.descriptor import RequestDescriptor
from models.runtime.request.state import RequestState
from models.runtime.spider.context import SpiderContext

@dataclass(slots=True)
class RequestContext:

    spider: SpiderContext

    descriptor: RequestDescriptor

    state: RequestState = field(
        default_factory=RequestState,
    )