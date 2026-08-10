from core.extraction.selector.extraction.base import ExtractionStrategy
from core.extraction.selector.extraction.mode import ExtractMode
from core.registry.single import SingletonPluginRegistry


class ExtractionRegistry(

    SingletonPluginRegistry[
        ExtractMode,
        ExtractionStrategy,
    ],

):
    pass