from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Sequence

import jmespath

from selector.config.base import SelectorConfig

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

    async def jmespath(self, selector: SelectorConfig) -> Any:
        """JMESPath 提取"""

        return jmespath.search(
            selector.selector,
            await self.json(),
        )
    
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