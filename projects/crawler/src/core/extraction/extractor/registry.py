from typing import Any

from core.request.discovery.registry import SingletonPluginRegistry
from core.extraction.extractor.base import Extractor
from models.enums.extract_type import ExtractType

class ExtractorRegistry(
    SingletonPluginRegistry[
        ExtractType,
        Extractor[Any],
    ],
):
    pass