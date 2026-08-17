from __future__ import annotations
from abc import ABC, abstractmethod
from jsonpath_ng.ext import parse
import jmespath
import re
from typing import Any

from core.extraction.response.base import ResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.config import SelectorConfig
from core.extraction.selector.typing import SelectorType


class StaticResponseAdapter(
    ResponseAdapter,
    ABC,
):
    """
    Base adapter for static responses.

    Provides selector capabilities that do not depend
    on a browser runtime.
    """

    def __init__(self) -> None:

        super().__init__()

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

    @abstractmethod
    async def content(
        self,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def json(
        self,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def root(
        self,
    ) -> NodeAdapter:
        raise NotImplementedError

    async def _select_regex(
        self,
        selector: SelectorConfig,
    ) -> Any:

        content = await self.content()

        if selector.selection == "multiple":

            return re.findall(
                selector.selector,
                content,
            )

        match = re.search(
            selector.selector,
            content,
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
    ) -> Any:

        data = await self.json()

        return jmespath.search(
            selector.selector,
            data,
        )

    async def _select_jsonpath(
        self,
        selector: SelectorConfig,
    ) -> Any:

        data = await self.json()

        expression = parse(
            selector.selector,
        )

        matches = expression.find(
            data,
        )

        if not matches:
            return None

        return [
            match.value
            for match in matches
        ]

    async def close(
        self,
    ) -> None:
        return None