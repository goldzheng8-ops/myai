from models.enums.selector_type import SelectorType
from core.dispatch.dispatch_table import DispatchTable
from core.response.types import SelectorHandler



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