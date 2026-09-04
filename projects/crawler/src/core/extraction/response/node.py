from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence

from core.extraction.response.dispatch import StaticDispatchTable, RuntimeDispatchTable
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from parsel import Selector
from playwright.async_api import Locator

class NodeAdapter(ABC):

    @abstractmethod
    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:
        raise NotImplementedError

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

class StaticNodeAdapter(
    NodeAdapter,
):

    def __init__(
        self,
        selector: Selector,
    ) -> None:
        self._static_dispatch = (
            StaticDispatchTable()
        )


        self._selector = selector

        self._static_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )

        self._static_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )
    @property
    def selector(
        self,
    ) -> Selector:
        return self._selector

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        handler = self._static_dispatch.dispatch(
            selector.type,
        )

        return await handler(selector)
    
    async def text(
        self,
    ) -> str | None:

        return self._selector.xpath(
            "string(.)",
        ).get()

    async def html(
        self,
    ) -> str:

        return self._selector.get()

    async def attribute(
        self,
        name: str,
    ) -> str | None:

        return self._selector.attrib.get(
            name,
        )

    async def _css_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        return [
            StaticNodeAdapter(node)
            for node in self._selector.css(
                selector.selector,
            )
        ]

    async def _xpath_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        return [
            StaticNodeAdapter(node)
            for node in self._selector.xpath(
                selector.selector,
            )
        ]

class PlaywrightNodeAdapter(NodeAdapter):

    def __init__(self, locator: Locator):

        self._locator = locator
        self._runtime_dispatch = (
            RuntimeDispatchTable()
        )
        self._runtime_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._runtime_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )
    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        handler = self._runtime_dispatch.dispatch(
            selector.type,
        )

        return await handler(selector)
    
    async def attribute(
        self,
        name: str,
    ) -> str | None:

        return await self._locator.get_attribute(name)

    async def text(self) -> str | None:

        return await self._locator.text_content()

    async def html(
        self,
    ) -> str:

        return await self._locator.evaluate(
            "(element) => element.outerHTML",
        )

    async def _css_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        locator = self._locator.locator(
            selector.selector,
        )

        count = await locator.count()

        return [
            PlaywrightNodeAdapter(
                locator.nth(index),
            )
            for index in range(count)
        ]

    async def _xpath_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        locator = self._locator.locator(
            f"xpath={selector.selector}",
        )

        count = await locator.count()

        return [
            PlaywrightNodeAdapter(
                locator.nth(index),
            )
            for index in range(count)
        ]

