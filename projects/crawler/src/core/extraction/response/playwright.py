import asyncio
from core.extraction.response.browser import BrowserResponseAdapter
from core.request.response.model import BrowserResponse
from playwright.async_api import BrowserContext, Locator, Page
import json
from typing import Any
from collections.abc import Sequence

from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from core.extraction.response.node import NodeAdapter


class PlaywrightNodeAdapter(NodeAdapter):

    def __init__(self, locator: Locator):

        super().__init__()

        self._locator = locator

        self._node_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._node_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )

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

class PlaywrightResponseAdapter(
    BrowserResponseAdapter,
):

    def __init__(
        self,
        response: BrowserResponse,
    ) -> None:
        super().__init__()

        if response.page is None:
            raise ValueError(
                "BrowserResponse.page is required.",
            )

        if response.browser_context is None:
            raise ValueError(
                "BrowserResponse.browser_context "
                "is required.",
            )

        self._response = response
        self._page = response.page
        self._browser_context = (
            response.browser_context
        )

        self._json_cache: Any | None = None


        self._node_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._node_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )

    @property
    def page(
        self,
    ) -> Page:

        return self._page

    @property
    def browser_context(
        self,
    ) -> BrowserContext:
        return self._browser_context

    async def content(
        self,
    ) -> str:

        return await self._page.content()



    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = json.loads(
                await self.content()
            )

        return self._json_cache
    
    async def root(
        self,
    ) -> NodeAdapter:

        return PlaywrightNodeAdapter(
            self._page.locator("html"),
        )

    async def scroll(
        self,
        *,
        count: int = 1,
        delay: float = 0.5,
    ):

        for _ in range(count):

            await self._page.mouse.wheel(
                0,
                5000,
            )

            await asyncio.sleep(delay)


    async def close(
        self,
    ) -> None:
        await self._browser_context.close()

    async def _css_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        locator = self._page.locator(
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

        locator = self._page.locator(
            f"xpath={selector.selector}",
        )

        count = await locator.count()


        return [
            PlaywrightNodeAdapter(
                locator.nth(index),
            )
            for index in range(count)
        ]

