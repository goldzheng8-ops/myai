from collections.abc import Callable
from typing import Any, TypeAlias

from core.extraction.transform.base import TransformPlugin

TransformFactory: TypeAlias = Callable[
    [],
    TransformPlugin[Any, Any, Any],
]

