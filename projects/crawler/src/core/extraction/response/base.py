from abc import ABC
from typing import Any, Sequence

from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from core.extraction.response.node import NodeAdapter
from core.extraction.response.dispatch import SelectorDispatchTable, NodeDispatchTable

class ResponseAdapter(ABC):

    def __init__(
        self,
    ):
        self._selector_dispatch = (
            SelectorDispatchTable()
        )
        self._node_dispatch = (
            NodeDispatchTable()
        )

    async def select(
        self,
        selector: SelectorConfigUnion,
    ) -> Any:

        handler = (
            self._selector_dispatch.dispatch(
                selector.type
            )
        )

        return await handler(
            selector,
        )

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:
        handler = (
            self._node_dispatch.dispatch(
                selector.type
            )
        )

        return await handler(
            selector,
        )


    async def content(
        self,
    ) -> str:
        raise NotImplementedError


    async def html(
        self,
    ) -> str:

        return await self.content()


    async def xml(
        self,
    ) -> str:

        return await self.content()


    async def json(
        self,
    ) -> Any:
        raise NotImplementedError

    async def root(
        self,
    ) -> NodeAdapter:
        raise NotImplementedError
        
    def is_node_selector(
        self,
        selector_type: SelectorType,
    ) -> bool:
        return self._node_dispatch.contains(selector_type)

    async def close(
        self,
    ) -> None:
        return None
    