from __future__ import annotations

from collections.abc import Awaitable, Callable
from enum import Enum
from typing import Any, TypeAlias, TypeVar

from core.runtime.context import RuntimeContext

ContextT = TypeVar(
    "ContextT",bound=RuntimeContext,
)

NodeId: TypeAlias = str

Metadata: TypeAlias = dict[str, Any]

WorkflowNext: TypeAlias = Callable[
    [ContextT],
    Awaitable[ContextT],
]

class WorkflowExecutionMode(str,Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    AUTO = "auto"