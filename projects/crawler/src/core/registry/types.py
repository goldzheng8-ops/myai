from collections.abc import Callable
from typing import TypeAlias, TypeVar

from core.plugin.base import Plugin

K = TypeVar("K")

V = TypeVar("V")

P = TypeVar(
    "P",
    bound=Plugin,
)

Provider: TypeAlias = Callable[[], P]