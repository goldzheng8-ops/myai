from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Sequence

from enums.selector_type import SelectorType
import jmespath
from config.selector.base import SelectorConfig


class NodeAdapter(ABC):

    @abstractmethod
    async def attribute(
        self,
        name: str,
    ) -> str | None:
        ...

    @abstractmethod
    async def text(self) -> str | None:
        ...

    @abstractmethod
    async def html(self) -> str:
        ...

class ResponseAdapter(ABC):

    @abstractmethod
    async def css(self, selector: SelectorConfig) -> Any:
        """CSS 选择器"""

    @abstractmethod
    async def xpath(self, selector: SelectorConfig) -> Any:
        """XPath 选择器"""

    @abstractmethod
    async def html(self) -> str:
        ...
        
    @abstractmethod
    async def json(self) -> Any:
        """返回 JSON"""

    async def regex(self, selector: SelectorConfig) -> Any:
        """Regex 提取"""

        content = await self.html()

        if selector.many:
            return re.findall(selector.selector, content)

        match = re.search(selector.selector, content)

        if match is None:
            return None

        return match.group(1) if match.groups() else match.group(0)

    
    async def _extract(
        self,
        node: NodeAdapter,
        selector: SelectorConfig,
    ) -> Any:

        if selector.attribute:
            return await node.attribute(selector.attribute)

        if selector.extract == "html":
            return await node.html()

        return await node.text()
    
    async def _select(
        self,
        nodes: Sequence[NodeAdapter],
        selector: SelectorConfig,
    ) -> Any:

        if selector.many:
            return [
                await self._extract(node, selector)
                for node in nodes
            ]

        if not nodes:
            return None

        return await self._extract(nodes[0], selector)

    async def select(
        self,
        selector: SelectorConfig,
    ) -> Any:
        """
        JSON Selector 统一入口
        """

        data = await self.json()

        match selector.type:

            case SelectorType.JMESPATH:
                return jmespath.search(
                    selector.selector,
                    data,
                )

            case SelectorType.JSONPATH:
                from jsonpath_ng.ext import parse

                expr = parse(selector.selector)

                matches = expr.find(data)

                if not matches:
                    return None

                return [m.value for m in matches]

            case SelectorType.CSS:
                return self.css(selector)

            case SelectorType.XPATH:
                return self.xpath(selector)

            case SelectorType.REGEX:
                return self.regex(selector)

        raise ValueError(
            f"Unsupported json selector: {selector.type}"
        )

    async def scroll(
        self,
        *,
        count: int = 1,
        delay: float = 0.5,
    ) -> None:
        """
        默认什么都不做。

        Requests/Scrapy 可以直接忽略。

        Playwright Override。
        """