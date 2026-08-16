import json
import re
from typing import Any, Sequence

import jmespath

from core.extraction.response.base import ResponseAdapter
from core.extraction.response.node import NodeAdapter
from core.extraction.selector.config import SelectorConfig
from core.extraction.selector.typing import SelectorType
from core.request.response import RequestResponse

class StaticResponseAdapter(
    ResponseAdapter,
):
    """
    Adapter for static HTTP responses.

    This adapter contains no browser-specific behavior.
    """

    def __init__(
        self,
        response: RequestResponse,
    ) -> None:

        self._response = response

        self._text_cache: str | None = None
        self._json_cache: Any | None = None

    @property
    def response(
        self,
    ) -> RequestResponse:

        return self._response

    async def content(
        self,
    ) -> str:

        if self._text_cache is None:

            encoding = (
                self._response.encoding
                or "utf-8"
            )

            self._text_cache = (
                self._response.body.decode(
                    encoding,
                    errors="replace",
                )
            )

        return self._text_cache

    async def html(
        self,
    ) -> str:

        return await self.content()

    async def xml(
        self,
    ) -> str:

        return await self.content()

    async def json(
        self,
    ) -> Any:

        if self._json_cache is None:

            self._json_cache = json.loads(
                await self.content(),
            )

        return self._json_cache

    async def select(
        self,
        selector: SelectorConfig,
    ) -> Any:

        selector_type = selector.type

        if selector_type == SelectorType.REGEX:

            return await self._select_regex(
                selector,
            )

        if selector_type == SelectorType.JMESPATH:

            return await self._select_jmespath(
                selector,
            )

        if selector_type == SelectorType.JSONPATH:

            return await self._select_jsonpath(
                selector,
            )

        if self.is_node_selector(
            selector_type,
        ):

            return await self.select_nodes(
                selector,
            )

        raise TypeError(
            f"Unsupported selector type: "
            f"{selector_type}",
        )

    async def select_nodes(
        self,
        selector: SelectorConfig,
    ) -> Sequence[NodeAdapter]:

        raise NotImplementedError(
            "StaticResponseAdapter does not "
            "provide node selection yet.",
        )

    async def root(
        self,
    ) -> NodeAdapter:

        raise NotImplementedError(
            "StaticResponseAdapter does not "
            "provide a root node yet.",
        )

    def is_node_selector(
        self,
        selector_type: SelectorType,
    ) -> bool:

        return selector_type in {
            SelectorType.CSS,
            SelectorType.XPATH,
        }

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

        raise NotImplementedError(
            "JSONPath support has not been "
            "implemented for StaticResponseAdapter.",
        )
 