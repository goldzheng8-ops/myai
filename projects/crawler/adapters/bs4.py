from bs4 import Tag
from bs4 import BeautifulSoup

from adapters.base import ResponseAdapter
from config.config import SelectorConfig


class BeautifulSoupAdapter(ResponseAdapter):
    def __init__(self, soup: BeautifulSoup | Tag):
        self._soup = soup

    def select(self, selector: SelectorConfig) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        if selector.type == "xpath":
            raise NotImplementedError("XPath is not supported in BeautifulSoupAdapter.")
        elif selector.type == "css":
            elements = self._soup.select(selector.query)
            return [element.get_text() for element in elements] if selector.many else elements[0].get_text() if elements else None
        elif selector.type == "regex":
            import re
            matches = re.findall(selector.query, str(self._soup))
            return matches if selector.many else matches[0] if matches else None
        else:
            raise ValueError(f"Unsupported selector type: {selector.type}")