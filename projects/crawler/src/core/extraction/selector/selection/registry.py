

from core.extraction.selector.selection.base import SelectionStrategy
from core.extraction.selector.selection.mode import SelectionMode
from core.registry.base import Registry


class SelectionRegistry(

    Registry[
        SelectionMode,
        SelectionStrategy,
    ],

):
    pass