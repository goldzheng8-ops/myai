from httpcore import Response
from playwright.async_api import Page

from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig


class PlaywrightResponseAdapter(ResponseAdapter):

    def __init__(
        self,
        page: Page,
        response: Response | None,
    ):
        self._page = page
        self._response = response

    def select(self, selector: SelectorConfig) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        if selector.type == "xpath":
            return self._page.locator(selector.query).all_inner_texts() if selector.many else self._page.locator(selector.query).inner_text()
        elif selector.type == "css":
            return self._page.locator(selector.query).all_inner_texts() if selector.many else self._page.locator(selector.query).inner_text()
        elif selector.type == "regex":
            import re
            text = self._page.content()
            matches = re.findall(selector.query, text)
            return matches if selector.many else matches[0] if matches else None
        else:
            raise ValueError(f"Unsupported selector type: {selector.type}")