from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeAlias

from core.provider.protocol import Resolver
from core.typing.vars import T


ProviderFactory: TypeAlias = Callable[[Resolver[Any, Any]], T]

ProviderFactories: TypeAlias = dict[
    type[Any],
    ProviderFactory[Any],
]