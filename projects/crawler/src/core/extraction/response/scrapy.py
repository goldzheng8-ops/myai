from __future__ import annotations

import json
from typing import Any, Sequence

from scrapy.http import Response

from core.extraction.response.static import StaticResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.response.node.scrapy import (
    ScrapyNodeAdapter,
)
from core.extraction.selector.config import SelectorConfig
from core.extraction.selector.typing import SelectorType


class ScrapyResponseAdapter(
    StaticResponseAdapter,
):
    """
    Extraction adapter for Scrapy responses.
    """

    def __init__(
        self,
        response: Response,
    ) -> None:

        self._response = response

        self._json_cache: Any | None = None

    @property
    def response(
        self,
    ) -> Response:

        return self._response

    async def content(
        self,
    ) -> str:

        encoding = (
            self._response.encoding
            or "utf-8"
        )

        return self._response.body.decode(
            encoding,
            errors="replace",
        )

    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = json.loads(
                await self.content(),
            )

        return self._json_cache

    async def select_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        if selector.type == SelectorType.CSS:

            nodes = self._response.css(
                selector.selector,
            )

            return [
                ScrapyNodeAdapter(node)
                for node in nodes
            ]

        if selector.type == SelectorType.XPATH:

            nodes = self._response.xpath(
                selector.selector,
            )

            return [
                ScrapyNodeAdapter(node)
                for node in nodes
            ]

        raise TypeError(
            f"Unsupported node selector: "
            f"{selector.type}",
        )

    async def root(
        self,
    ) -> NodeAdapter:

        return ScrapyNodeAdapter(
            self._response,
        )