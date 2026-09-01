from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, TypeAlias, TypeVar

from core.runtime.context import RuntimeContext

if TYPE_CHECKING:
    from .runtime import PipelineRuntime

ContextT = TypeVar(
    "ContextT",
    bound=RuntimeContext,
)

PipelineNext: TypeAlias = Callable[
    [
        ContextT,
        "PipelineRuntime",
    ],
    Awaitable[ContextT],
]