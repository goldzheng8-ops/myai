from __future__ import annotations

import json
from typing import Any, Sequence
from core.request.response.model import ScrapyResponse
from scrapy.http import Response
from parsel.selector import Selector

from core.extraction.response.static import StaticResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType

class ScrapyNodeAdapter(
    NodeAdapter,
):

    def __init__(
        self,
        selector: Selector,
    ) -> None:

        super().__init__()

        self._selector = selector

        self._node_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )

        self._node_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )

    async def text(
        self,
    ) -> str | None:

        values = self._selector.xpath(
            "string(.)",
        ).get()

        if values is None:
            return None

        return values

    async def html(
        self,
    ) -> str:

        value = self._selector.get()

        return value

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

        nodes = self._selector.css(
            selector.selector,
        )

        return [
            ScrapyNodeAdapter(
                node,
            )
            for node in nodes
        ]

    async def _xpath_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        nodes = self._selector.xpath(
            selector.selector,
        )

        return [
            ScrapyNodeAdapter(
                node,
            )
            for node in nodes
        ]

class ScrapyResponseAdapter(
    StaticResponseAdapter,
):
    """
    Extraction adapter for a Scrapy response.

    This adapter bridges Scrapy's native Response
    into the generic extraction API.
    """

    def __init__(
        self,
        response: ScrapyResponse,
    ) -> None:

        super().__init__()

        self._response = response.raw

        self._json_cache: Any | None = None

    @property
    def response(
        self,
    ) -> Response:

        return self._response

    async def content(
        self,
    ) -> str:

        return self._response.text

    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = json.loads(
                await self.content(),
            )

        return self._json_cache

    async def root(
        self,
    ) -> NodeAdapter:

        return ScrapyNodeAdapter(
            self._selector(),
        )

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        if selector.type == SelectorType.CSS:

            nodes = self._response.css(
                selector.selector,
            )

            return [
                ScrapyNodeAdapter(
                    node,
                )
                for node in nodes
            ]

        if selector.type == SelectorType.XPATH:

            nodes = self._response.xpath(
                selector.selector,
            )

            return [
                ScrapyNodeAdapter(
                    node,
                )
                for node in nodes
            ]

        raise TypeError(
            "Unsupported node selector: "
            f"{selector.type!r}",
        )

    def _selector(self) -> Selector:
        return Selector(
            text=self._response.text,
        )