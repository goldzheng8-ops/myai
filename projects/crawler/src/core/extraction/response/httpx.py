from __future__ import annotations

import json
from typing import Any, Sequence

import httpx

from core.extraction.response.static import StaticResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.response.node.httpx import HttpxNodeAdapter
from core.extraction.selector.config import SelectorConfig


class HttpxResponseAdapter(
    StaticResponseAdapter,
):
    """
    Extraction adapter for httpx responses.
    """

    def __init__(
        self,
        response: httpx.Response,
    ) -> None:

        self._response = response

        self._json_cache: Any | None = None

    @property
    def response(
        self,
    ) -> httpx.Response:

        return self._response

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

    async def select_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        raise NotImplementedError(
            "HTML node selection for HTTPX "
            "requires an HTML parser.",
        )

    async def root(
        self,
    ) -> NodeAdapter:

        raise NotImplementedError(
            "HTTPX root node requires an HTML parser.",
        )