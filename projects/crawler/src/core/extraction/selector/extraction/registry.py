from core.extraction.selector.extraction.base import ExtractionStrategy
from core.extraction.selector.extraction.mode import ExtractMode
from core.registry.base import Registry


class ExtractionRegistry(

    Registry[
        ExtractMode,
        ExtractionStrategy,
    ],

):
    pass