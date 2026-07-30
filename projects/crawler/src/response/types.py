from collections.abc import Awaitable, Callable
from typing import Any, Sequence, TypeAlias

from config.selector.base import SelectorConfig
from response.node import NodeAdapter

ValueSelectorHandler: TypeAlias = Callable[
    [SelectorConfig],
    Awaitable[Any],
]

NodeSelectorHandler: TypeAlias = Callable[
    [SelectorConfig],
    Awaitable[Sequence[NodeAdapter]],
]



ExtractionHandler: TypeAlias = Callable[
    [
        NodeAdapter,
        SelectorConfig,
    ],
    Awaitable[Any],
]

SelectorHandler: TypeAlias = Callable[
    [
        SelectorConfig,
    ],
    Awaitable[Any],
]