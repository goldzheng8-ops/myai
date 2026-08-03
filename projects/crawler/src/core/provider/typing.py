from collections.abc import Callable
from typing import Any, TypeAlias, TypeVar

from core.provider.manager import ProviderManager
T = TypeVar("T")

ProviderFactory: TypeAlias = Callable[[ProviderManager], T]

ProviderFactories: TypeAlias = dict[
    type[Any],
    ProviderFactory[Any],
]