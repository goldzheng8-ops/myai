from abc import ABC, abstractmethod
from typing import Sequence

from core.extraction.response.node import NodeAdapter
from core.extraction.response.dispatch import NodeDispatchTable
from core.extraction.selector.config import SelectorConfig

class NodeAdapter(ABC):

    def __init__(
        self,
    ):
        self._node_dispatch = (
            NodeDispatchTable()
        )

    @abstractmethod
    async def css_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:
        ...

    @abstractmethod
    async def xpath_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:
        ...

    async def select_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        handler = self._node_dispatch.dispatch(
            selector.type,
        )

        return await handler(selector)

    @abstractmethod
    async def text(self) -> str | None:
        ...

    @abstractmethod
    async def html(self) -> str:
        ...

    @abstractmethod
    async def attribute(
        self,
        name: str,
    ) -> str | None:
        ...