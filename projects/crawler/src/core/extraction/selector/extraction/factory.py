from collections.abc import Callable
from typing import TypeAlias

from core.extraction.selector.extraction.base import ExtractionStrategy


ExtractionFactory: TypeAlias = Callable[
    [],
    ExtractionStrategy,
]