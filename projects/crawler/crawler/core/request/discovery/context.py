from dataclasses import dataclass

from core.extraction.response.base import ResponseAdapter
from core.request.context import RequestContext
from core.runtime import RuntimeContext

@dataclass(frozen=True, slots=True)
class DiscoveryContext:
    request: RequestContext | None = None
    response: ResponseAdapter | None = None

    @property
    def runtime(self) -> RuntimeContext | None:
        if self.request is None:
            return None

        return self.request.runtime