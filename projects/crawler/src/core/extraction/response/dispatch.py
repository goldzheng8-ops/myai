from core.extraction.selector.typing import SelectorType
from core.registry.dispatch import DispatchTable
from core.extraction.response.types import SelectorHandler



class SelectorDispatchTable(
    DispatchTable[
        SelectorType,
        SelectorHandler,
    ],
):
    ...

class NodeDispatchTable(
    DispatchTable[
        SelectorType,
        SelectorHandler,
    ],
):
    ...