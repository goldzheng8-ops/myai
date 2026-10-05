from __future__ import annotations

from dataclasses import dataclass, field



from core.request.response import RequestResponse
from core.request.result import RequestResult
from core.runtime import RuntimeContext
from core.spider.config import SpiderConfigUnion

from .descriptor import RequestDescriptor
from .state import RequestState

@dataclass(slots=True)
class RequestContext:
    """
    Runtime context of a single request execution.
    """

    descriptor: RequestDescriptor

    config: SpiderConfigUnion
    
    runtime: RuntimeContext 

    fingerprint: str | None = None

    session_id: str | None = None


    state: RequestState = field(
        default_factory=RequestState,
    )

    transport_response: RequestResponse | None = None
    
    result: RequestResult | None = None