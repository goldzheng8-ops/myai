from dataclasses import dataclass, field, replace

from response.base import ResponseAdapter
from response.node import NodeAdapter
from core.context.request_context import RequestContext
from core.context.runtime_context import RuntimeContext



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
