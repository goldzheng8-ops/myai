from models.enums.selector_type import SelectorType
from core.registry.dispatch import DispatchTable
from core.request.response.types import SelectorHandler



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