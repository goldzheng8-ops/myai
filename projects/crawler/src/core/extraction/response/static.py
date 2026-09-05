from __future__ import annotations
from collections.abc import Mapping, Sequence
import json

from core.request.response.model import RequestResponse
from jsonpath_ng.ext import parse
import jmespath
import re
from typing import Any

from core.extraction.response.base import ResponseAdapter
from core.extraction.response.node import NodeAdapter, StaticNodeAdapter
from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from parsel import Selector



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
        self._static_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._static_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )
    @property
    def response(
        self,
    ) -> RequestResponse:
        return self._response
    @property
    def url(self) -> str:
        return self._response.url

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> Mapping[str, str]:
        return self._response.headers

    @property
    def body(self) -> bytes:
        return self._response.body

    @property
    def encoding(self) -> str | None:
        return self._response.encoding
    
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

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        handler = self._static_dispatch.dispatch(
            selector.type,
        )

        return await handler(selector)
    
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

    async def _css_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        return [
            StaticNodeAdapter(node)
            for node in self._selector().css(
                selector.selector,
            )
        ]

    async def _xpath_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        return [
            StaticNodeAdapter(node)
            for node in self._selector().xpath(
                selector.selector,
            )
        ]

    async def close(
        self,
    ) -> None:
        return None