from dataclasses import dataclass

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.runtime import RuntimeContext


@dataclass(frozen=True, slots=True)
class TransformContext:

    request: RequestContext

    @property
    def runtime(self) -> RuntimeContext:
        return self.request.runtime

    @property
    def descriptor(self) -> RequestDescriptor:
        return self.request.descriptor