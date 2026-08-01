
import asyncio
import re
from models.enums.selector_type import SelectorType
import jmespath
from jsonpath_ng.ext import parse

from models.config.selector.base import SelectorConfig
from playwright.async_api import Locator, Page
import json
from typing import Any, Sequence

from models.runtime.response.base import ResponseAdapter
from models.runtime.response.node import NodeAdapter


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

    async def css_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        locator = self._locator.locator(
            selector.selector,
        )

        count = await locator.count()

        return [
            PlaywrightNodeAdapter(
                locator.nth(i),
            )
            for i in range(count)
        ]

    async def xpath_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        locator = self._locator.locator(
            f"xpath={selector.selector}",
        )

        count = await locator.count()

        return [
            PlaywrightNodeAdapter(
                locator.nth(i),
            )
            for i in range(count)
        ]

class PlaywrightResponseAdapter(
    ResponseAdapter,
):

    def __init__(
        self,
        page: Page,
    ) -> None:

        self._page = page

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
        self._node_dispatch.register(
            SelectorType.CSS,
            self._css_nodes,
        )
        self._node_dispatch.register(
            SelectorType.XPATH,
            self._xpath_nodes,
        )

    async def root(
        self,
    ) -> NodeAdapter:

        return PlaywrightNodeAdapter(
            self._page.locator("html"),
        )

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

    async def _css_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        locator = self._page.locator(
            selector.selector,
        )

        count = await locator.count()


        return [
            PlaywrightNodeAdapter(
                locator.nth(i),
            )
            for i in range(count)
        ]



    async def _xpath_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        locator = self._page.locator(
            f"xpath={selector.selector}",
        )

        count = await locator.count()


        return [
            PlaywrightNodeAdapter(
                locator.nth(i),
            )
            for i in range(count)
        ]

    async def _select_regex(
        self,
        selector: SelectorConfig,
    ):

        html = await self.html()


        if selector.selection == "multiple":

            return re.findall(
                selector.selector,
                html,
            )


        match = re.search(
            selector.selector,
            html,
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
        selector: SelectorConfig,
    ):

        data = await self.json()

        return jmespath.search(
            selector.selector,
            data,
        )



    async def _select_jsonpath(
        self,
        selector: SelectorConfig,
    ):

        data = await self.json()

        expr = parse(
            selector.selector,
        )

        matches = expr.find(
            data,
        )


        if not matches:
            return None


        return [
            item.value
            for item in matches
        ]