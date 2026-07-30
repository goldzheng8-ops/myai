

from core.pipeline.selection.base import SelectionStrategy
from core.pipeline.selection.mode import SelectionMode
from core.registry.single import SingletonPluginRegistry


class SelectionRegistry(

    SingletonPluginRegistry[
        SelectionMode,
        SelectionStrategy,
    ],

):
    pass