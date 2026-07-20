from abc import ABC, abstractmethod
from functools import cached_property
import re
from typing import Any

from jsonpath_ng.ext import parse

from config.config import SelectorConfig


class ResponseAdapter(ABC):

    @abstractmethod
    def css(
        self,
        selector: SelectorConfig,
    ) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        raise NotImplementedError
    

    @abstractmethod
    def xpath(
        self,
        selector: SelectorConfig,
    ) -> Any:
        """
        根据 SelectorConfig 提取数据
        """
        raise NotImplementedError
    
    @abstractmethod
    def text(self) -> str:
        """返回页面文本"""

    @abstractmethod
    def html(self) -> str:
        """返回页面 HTML"""
    
    @cached_property
    @abstractmethod
    def json(self) -> Any:
        ...

    def regex(self, selector: SelectorConfig):

        html = self.html()

        if selector.many:
            return re.findall(selector.selector, html)

        match = re.search(selector.selector, html)

        if match is None:
            return None

        if match.groups():
            return match.group(1)

        return match.group(0)
    

    def jsonpath(self, selector: SelectorConfig) -> Any:

        expr = parse(selector.selector)

        result = [
            match.value
            for match in expr.find(self.json())
        ]

        if selector.many:
            return result

        return result[0] if result else None