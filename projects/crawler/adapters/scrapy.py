
from scrapy.http import Response
from typing import Any

from adapters.base import ResponseAdapter
from config.config import SelectorConfig
from scrapy.selector import Selector

class ScrapyResponseAdapter(ResponseAdapter):

    def __init__(self, node: Response | Selector):
        self._node = node


    def select(
    self,
    selector: SelectorConfig,
    ) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        if selector.type == "xpath":
            return self._node.xpath(selector.query).getall() if selector.many else self._node.xpath(selector.query).get()
        elif selector.type == "css":
            return self._node.css(selector.query).getall() if selector.many else self._node.css(selector.query).get()
        elif selector.type == "regex":
            return self._node.re(selector.query) if selector.many else self._node.re_first(selector.query)
        else:
            raise ValueError(f"Unsupported selector type: {selector.type}")

