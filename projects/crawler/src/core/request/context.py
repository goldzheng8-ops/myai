from __future__ import annotations

from dataclasses import dataclass, field



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
    runtime: RuntimeContext = field(
        default_factory=RuntimeContext,
    )

    fingerprint: str | None = None

    session_id: str | None = None


    state: RequestState = field(
        default_factory=RequestState,
    )

    result: RequestResult | None = None