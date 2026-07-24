

from typing import Any

from adapters.base import ResponseAdapter
from config.selector.base import SelectorConfig
from enums.selector_type import SelectorType


class SelectorDispatcher:

    @classmethod
    async def select(
        cls,
        response: ResponseAdapter,
        selector: SelectorConfig,
    ) -> Any:

        match selector.type:

            case SelectorType.CSS:
                return await response.css(selector)

            case SelectorType.XPATH:
                return await response.xpath(selector)

            case SelectorType.REGEX:
                return await response.regex(selector)

            case SelectorType.JMESPATH:
                return await response.select_json(selector)

            case _:
                raise ValueError(...)