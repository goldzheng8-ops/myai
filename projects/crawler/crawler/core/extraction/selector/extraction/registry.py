from core.extraction.selector.extraction.base import ExtractionStrategy
from core.extraction.selector.extraction.factory import ExtractionFactory
from core.extraction.selector.extraction.mode import ExtractMode
from core.registry.base import Registry


class ExtractionRegistry(
    Registry[
        ExtractMode,
        ExtractionFactory,
    ],
):
    """
    Registry of extraction strategy factories.
    """

    def create(
        self,
        mode: ExtractMode,
    ) -> ExtractionStrategy:

        return self.get(mode)()