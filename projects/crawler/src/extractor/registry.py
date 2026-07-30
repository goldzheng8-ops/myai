from typing import Any

from discovery.registry import SingletonPluginRegistry
from extractor.base import Extractor
from enums.extract_type import ExtractType

class ExtractorRegistry(
    SingletonPluginRegistry[
        ExtractType,
        Extractor[Any],
    ],
):
    pass