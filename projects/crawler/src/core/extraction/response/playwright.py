import asyncio
from core.extraction.response.browser import BrowserResponseAdapter


from core.request.response.model import BrowserResponse,RequestResponse
from playwright.async_api import BrowserContext, Page
import json
from typing import Any
from collections.abc import Sequence

from core.extraction.selector.config import SelectorConfigUnion
from core.extraction.selector.typing import SelectorType
from core.extraction.response.node import NodeAdapter, PlaywrightNodeAdapter, StaticNodeAdapter




class PlaywrightResponseAdapter(
    BrowserResponseAdapter,
):

    def __init__(
        self,
        response: RequestResponse,
    ) -> None:
        super().__init__(response)

        if isinstance(response, BrowserResponse):
            if response.page is None:
                raise ValueError(
                    "BrowserResponse.page is required."
                )

            if response.browser_context is None:
                raise ValueError(
                    "BrowserResponse.browser_context is required."
                )

            self._page = response.page
            self._browser_context = response.browser_context

        else:
            self._page = None
            self._browser_context = None

        self._runtime_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._runtime_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )
        
    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError(
                "Browser page is unavailable for "
                "a cached response.",
            )
        return self._page

    @property
    def browser_context(self) -> BrowserContext:
        if self._browser_context is None:
            raise RuntimeError(
                "Browser context is unavailable for "
                "a cached response.",
            )
        return self._browser_context

    async def select_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:

        if self._page is not None:
            handler = self._runtime_dispatch.dispatch(
                selector.type,
            )
            return await handler(selector)

        handler = self._static_dispatch.dispatch(
            selector.type,
        )
        return await handler(selector)

    async def content(self) -> str:
        if self._page is not None:
            return await self._page.content()
        return self._response.text


    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = json.loads(
                await self.content()
            )

        return self._json_cache
    
    async def root(self) -> NodeAdapter:

        if self._page is not None:
            return PlaywrightNodeAdapter(
                self._page.locator("html"),
            )

        return StaticNodeAdapter(
            self._selector(),
        )
    async def scroll(
        self,
        *,
        count: int = 1,
        delay: float = 0.5,
    ) -> None:

        for _ in range(count):

            await self.page.mouse.wheel(
                0,
                5000,
            )

            await asyncio.sleep(delay)


    async def close(
        self,
    ) -> None:
        if self._browser_context is not None:
            await self._browser_context.close()

    async def _css_nodes(
        self,
        selector: SelectorConfigUnion,
    ) -> Sequence[NodeAdapter]:


        locator = self.page.locator(
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

        locator = self.page.locator(
            f"xpath={selector.selector}",
        )

        count = await locator.count()


        return [
            PlaywrightNodeAdapter(
                locator.nth(index),
            )
            for index in range(count)
        ]

