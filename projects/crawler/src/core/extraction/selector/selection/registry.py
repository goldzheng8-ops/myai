

from core.extraction.selector.selection.base import SelectionStrategy
from core.extraction.selector.selection.mode import SelectionMode
from core.registry.single import SingletonPluginRegistry


class SelectionRegistry(

    SingletonPluginRegistry[
        SelectionMode,
        SelectionStrategy,
    ],

):
    pass