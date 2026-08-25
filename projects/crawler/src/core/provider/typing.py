from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeAlias

from core.provider.protocol import ProviderResolver
from core.typing.vars import T


ProviderFactory: TypeAlias = Callable[[ProviderResolver[Any, Any]], T]

ProviderFactories: TypeAlias = dict[
    type[Any],
    ProviderFactory[Any],
]