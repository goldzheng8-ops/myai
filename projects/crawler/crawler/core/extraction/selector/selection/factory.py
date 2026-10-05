from collections.abc import Callable
from typing import TypeAlias

from core.extraction.selector.selection.base import SelectionStrategy


SelectionFactory: TypeAlias = Callable[
    [],
    SelectionStrategy,
]