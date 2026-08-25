from typing import Any

from core.extraction.extractor.factory import ExtractorFactory
from core.registry.base import Registry
from core.extraction.extractor.base import Extractor
from .typing import ExtractType

class ExtractorRegistry(
    Registry[
        ExtractType,
        ExtractorFactory,
    ],
):
    """
    Registry of extractor factories.
    """

    def create(
        self,
        type_: ExtractType,
    ) -> Extractor[Any]:

        return self.get(type_)()