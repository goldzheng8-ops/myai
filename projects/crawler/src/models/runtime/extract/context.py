from dataclasses import dataclass, field, replace

from core.response.base import ResponseAdapter
from core.response.node import NodeAdapter
from core.request.context import RequestContext
from models.runtime.extract.runtime import RuntimeContext



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
