from dataclasses import dataclass, field, replace

from core.extraction.response.base import ResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.request.context import RequestContext
from core.runtime import RuntimeContext



@dataclass(slots=True)
class ExtractContext:

    request: RequestContext

    response: ResponseAdapter

    node: NodeAdapter | None = None

    runtime: RuntimeContext = field(
        default_factory=RuntimeContext,
    )

    def with_node(
        self,
        node: NodeAdapter | None,
    ) -> "ExtractContext":

        return replace(
            self,
            node=node,
        )
