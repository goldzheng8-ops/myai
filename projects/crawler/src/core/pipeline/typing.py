from collections.abc import Awaitable, Callable
from typing import TypeVar

from core.pipeline.context import PipelineContext

ContextT = TypeVar(
    "ContextT",
    bound=PipelineContext,
)

Next = Callable[
    [ContextT],
    Awaitable[ContextT],
]