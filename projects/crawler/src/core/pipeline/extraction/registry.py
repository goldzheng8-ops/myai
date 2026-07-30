from core.pipeline.extraction.base import ExtractionStrategy
from core.pipeline.extraction.mode import ExtractMode
from core.registry.single import SingletonPluginRegistry


class ExtractionRegistry(

    SingletonPluginRegistry[
        ExtractMode,
        ExtractionStrategy,
    ],

):
    pass