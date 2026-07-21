from playwright.async_api import Locator, Page
import json
from typing import Any

from adapters.base import NodeAdapter, ResponseAdapter
from config.config import SelectorConfig


from playwright.async_api import Locator


class PlaywrightNodeAdapter(NodeAdapter):

    def __init__(self, locator: Locator):
        self._locator = locator

    async def attribute(
        self,
        name: str,
    ) -> str | None:

        return await self._locator.get_attribute(name)

    async def text(self) -> str | None:

        return await self._locator.text_content()

    async def html(self) -> str:

        return await self._locator.inner_html()

class PlaywrightResponseAdapter(ResponseAdapter):

    def __init__(
        self,
        page: Page
    ):
        self._page = page
        self._json_cache: Any | None = None

    async def css(self, selector: SelectorConfig) -> Any:
        locator = self._page.locator(selector.selector)
        count = await locator.count()

        nodes = [
            PlaywrightNodeAdapter(
                locator.nth(i)
            )
            for i in range(count)
        ]

        return await self._select(
            nodes,
            selector,
        )



    async def xpath(self, selector: SelectorConfig) -> Any:
        locator = self._page.locator(f"xpath={selector.selector}")
        count = await locator.count()
        nodes = [
            PlaywrightNodeAdapter(
                locator.nth(i)
            )
            for i in range(count)
        ]

        return await self._select(
            nodes,
            selector,
        )

    async def html(self) -> str:
        return await self._page.content()
    
    async def json(self) -> Any:
        if self._json_cache is None:
            self._json_cache = json.loads(
                await self.html()
            )

        return self._json_cache



    
