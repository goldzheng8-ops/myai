from core.extraction.selector.typing import SelectorType
from core.registry.dispatch import DispatchTable
from core.extraction.response.typing import SelectorHandler



class SelectorDispatchTable(
    DispatchTable[
        SelectorType,
        SelectorHandler,
    ],
):
    ...

class StaticDispatchTable(
    DispatchTable[
        SelectorType,
        SelectorHandler,
    ],
):
    ...

class RuntimeDispatchTable(
    DispatchTable[
        SelectorType,
        SelectorHandler,
    ],
):
    ...