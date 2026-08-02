from selector.extraction.base import ExtractionStrategy
from selector.extraction.mode import ExtractMode
from core.registry.single import SingletonPluginRegistry


class ExtractionRegistry(

    SingletonPluginRegistry[
        ExtractMode,
        ExtractionStrategy,
    ],

):
    pass