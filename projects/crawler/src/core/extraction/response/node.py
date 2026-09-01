from abc import ABC, abstractmethod
from typing import Sequence

from core.extraction.response.node import NodeAdapter
from core.extraction.response.dispatch import NodeDispatchTable
from core.extraction.selector.config import SelectorConfigUnion

class NodeAdapter(ABC):

    def __init__(
        self,
    ):
        self._node_dispatch = (
            NodeDispatchTable()
        )

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        handler = self._node_dispatch.dispatch(
            selector.type,
        )

        return await handler(selector)

    @abstractmethod
    async def text(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def html(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def attribute(
        self,
        name: str,
    ) -> str | None:
        raise NotImplementedError