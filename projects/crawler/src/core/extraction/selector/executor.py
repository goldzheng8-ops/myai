from typing import Any, Protocol, Sequence

from core.extraction.selector.config import SelectorConfig
from core.extraction.response.node import NodeAdapter

class PipelineExecutor(Protocol):

    async def execute(
        self,
        nodes: Sequence[NodeAdapter],
        selector: SelectorConfig,
    ) -> Any:
        ...