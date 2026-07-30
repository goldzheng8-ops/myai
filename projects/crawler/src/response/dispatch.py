from enums.selector_type import SelectorType
from core.dispatch.dispatch_table import DispatchTable
from response.types import SelectorHandler



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