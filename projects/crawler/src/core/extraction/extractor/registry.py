from typing import Any

from core.registry.base import Registry
from core.extraction.extractor.base import Extractor
from models.enums.extract_type import ExtractType

class ExtractorRegistry(
    Registry[
        ExtractType,
        Extractor[Any],
    ],
):
    pass