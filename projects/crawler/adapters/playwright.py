from playwright.async_api import Locator, Page
import json
from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig


class PlaywrightResponseAdapter(ResponseAdapter):

    def __init__(
        self,
        page: Page
    ):
        self._page = page

    def css(self, selector: SelectorConfig) -> Any:
        locator = self._page.locator(selector.selector)
        return self._select(locator, selector)



    def xpath(self, selector: SelectorConfig) -> Any:
        locator = self._page.locator(f"xpath={selector.selector}")
        return self._select(locator, selector)

    def html(self) -> str:
        return self._page.content()

    def text(self) -> str:
        return self._page.locator("body").text_content() or ""

    def json(self) -> Any:
        return json.loads(self.html())


    def _select(
            self,
            locator: Locator,
            selector: SelectorConfig,
        ) -> Any:
            count = locator.count()
            if count == 0:
                return [] if selector.many else None
            if selector.many:
                return [
                    self._extract(locator.nth(i), selector)
                    for i in range(count)
                ]
            return self._extract(locator.first, selector)
    
    def _extract(
        self,
        locator: Locator,
        selector: SelectorConfig,
    ) -> Any:
        if selector.attribute:
            return locator.get_attribute(selector.attribute)
        if selector.extract == "html":
            return locator.inner_html()
        return locator.text_content()