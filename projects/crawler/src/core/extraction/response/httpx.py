from __future__ import annotations

from typing import Any, Sequence
from core.request.response.model import HttpxResponse
import httpx
from parsel import Selector

from core.extraction.response.static import StaticResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType

class HttpxNodeAdapter(
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

    @property
    def selector(
        self,
    ) -> Selector:

        return self._selector

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

        nodes = self._selector.css(
            selector.selector,
        )

        return [
            HttpxNodeAdapter(node)
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
            HttpxNodeAdapter(node)
            for node in nodes
        ]

class HttpxResponseAdapter(
    StaticResponseAdapter,
):
    """
    Extraction adapter for an HTTPX response.

    HTTPX is treated as a static response source.
    HTML node extraction is delegated to Parsel through
    HttpxNodeAdapter.
    """

    def __init__(
        self,
        response: HttpxResponse,
    ) -> None:

        super().__init__()

        self._response = response.raw

        self._json_cache: Any | None = None

        self._selector_cache: Selector | None = None

    @property
    def response(
        self,
    ) -> httpx.Response:

        return self._response

    def _selector(
        self,
    ) -> Selector:

        if self._selector_cache is None:

            self._selector_cache = Selector(
                text=self._response.text,
            )

        return self._selector_cache

    async def content(
        self,
    ) -> str:

        return self._response.text

    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = self._response.json()

        return self._json_cache

    async def root(
        self,
    ) -> NodeAdapter:

        return HttpxNodeAdapter(
            self._selector(),
        )

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        root = self._selector()

        if selector.type == SelectorType.CSS:

            nodes = root.css(
                selector.selector,
            )

        elif selector.type == SelectorType.XPATH:

            nodes = root.xpath(
                selector.selector,
            )

        else:

            raise TypeError(
                "Unsupported node selector: "
                f"{selector.type!r}",
            )

        return [
            HttpxNodeAdapter(
                node,
            )
            for node in nodes
        ]
