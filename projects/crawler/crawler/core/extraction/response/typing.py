from collections.abc import Awaitable, Callable
from typing import Any,  TypeAlias



from core.extraction.selector.config import SelectorConfigUnion

# ValueSelectorHandler: TypeAlias = Callable[
#     [SelectorConfig],
#     Awaitable[Any],
# ]

# NodeSelectorHandler: TypeAlias = Callable[
#     [SelectorConfig],
#     Awaitable[Sequence[NodeAdapter]],
# ]



# ExtractionHandler: TypeAlias = Callable[
#     [
#         NodeAdapter,
#         SelectorConfig,
#     ],
#     Awaitable[Any],
# ]

SelectorHandler: TypeAlias = Callable[
    [
        SelectorConfigUnion,
    ],
    Awaitable[Any],
]

