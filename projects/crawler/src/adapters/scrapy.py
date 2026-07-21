
import json
from typing import Any
from scrapy.http import TextResponse

from adapters.base import NodeAdapter, ResponseAdapter
from selector.config.base import SelectorConfig

from parsel import Selector


class ScrapyNodeAdapter(NodeAdapter):

    def __init__(self, selector: Selector):
        self._selector = selector

    async def attribute(
        self,
        name: str,
    ) -> str | None:

        return self._selector.attrib.get(name)

    async def text(self) -> str | None:

        return self._selector.xpath("string(.)").get()

    async def html(self) -> str:

        return self._selector.get()

class ScrapyResponseAdapter(ResponseAdapter):

    def __init__(self, response: TextResponse):
        self._response = response
        self._json_cache: Any | None = None

    async def css(
        self,
        selector: SelectorConfig,
    ) -> Any:

        nodes = [
            ScrapyNodeAdapter(x)
            for x in self._response.css(selector.selector)
        ]

        return await self._select(
            nodes,
            selector,
        )
    

    async def xpath(
        self,
        selector: SelectorConfig,
    ) -> Any:
    
        nodes = [
            ScrapyNodeAdapter(x)
            for x in self._response.xpath(selector.selector)
        ]

        return await self._select(
            nodes,
            selector,
        )
    async def html(self) -> str:
        return self._response.text

    async def json(self) -> Any:

        if self._json_cache is None:
            self._json_cache = json.loads(
                self._response.text
            )

        return self._json_cache
        





