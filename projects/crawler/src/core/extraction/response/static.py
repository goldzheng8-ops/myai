from __future__ import annotations
from collections.abc import Sequence
import json
from core.request.response.model import RequestResponse
from jsonpath_ng.ext import parse
import jmespath
import re
from typing import Any

from core.extraction.response.base import ResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from parsel import Selector

class StaticNodeAdapter(
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

class StaticResponseAdapter(
    ResponseAdapter,
):
    """
    Base adapter for static response snapshots.

    The adapter operates on RequestResponse rather than
    downloader-specific runtime response objects.
    """

    def __init__(
        self,
        response: RequestResponse,
    ) -> None:

        super().__init__()

        self._response = response

        self._selector_cache: Selector | None = None
        self._json_cache: Any | None = None

        self._selector_dispatch.register(
            SelectorType.REGEX,
            self._select_regex,
        )

        self._selector_dispatch.register(
            SelectorType.JMESPATH,
            self._select_jmespath,
        )

        self._selector_dispatch.register(
            SelectorType.JSONPATH,
            self._select_jsonpath,
        )

    @property
    def response(
        self,
    ) -> RequestResponse:
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
                self._response.text,
            )

        return self._json_cache

    async def root(
        self,
    ) -> NodeAdapter:

        return StaticNodeAdapter(
            self._selector(),
        )

    def _selector(
        self,
    ) -> Selector:

        if self._selector_cache is None:
            self._selector_cache = Selector(
                text=self._response.text,
            )

        return self._selector_cache

    async def _select_regex(
        self,
        selector: SelectorConfigUnion,
    ) -> Any:

        content = await self.content()

        if selector.selection == "multiple":

            return re.findall(
                selector.selector,
                content,
            )

        match = re.search(
            selector.selector,
            content,
        )

        if match is None:
            return None

        return (
            match.group(1)
            if match.groups()
            else match.group(0)
        )

    async def _select_jmespath(
        self,
        selector: SelectorConfigUnion,
    ) -> Any:

        data = await self.json()

        return jmespath.search(
            selector.selector,
            data,
        )

    async def _select_jsonpath(
        self,
        selector: SelectorConfigUnion,
    ) -> Any:

        data = await self.json()

        expression = parse(
            selector.selector,
        )

        matches = expression.find(
            data,
        )

        if not matches:
            return None

        return [
            match.value
            for match in matches
        ]

    async def close(
        self,
    ) -> None:
        return None