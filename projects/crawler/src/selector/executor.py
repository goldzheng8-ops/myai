from typing import Any, Protocol, Sequence

from models.config.selector.base import SelectorConfig
from models.runtime.response.node import NodeAdapter

class PipelineExecutor(Protocol):

    async def execute(
        self,
        nodes: Sequence[NodeAdapter],
        selector: SelectorConfig,
    ) -> Any:
        ...