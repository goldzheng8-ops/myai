from typing import Any, Protocol, Sequence

from config.selector.base import SelectorConfig
from response.node import NodeAdapter

class PipelineExecutor(Protocol):

    async def execute(
        self,
        nodes: Sequence[NodeAdapter],
        selector: SelectorConfig,
    ) -> Any:
        ...