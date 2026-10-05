# core/event/typing.py

from __future__ import annotations

from enum import Enum
from typing import Any, TypeAlias, TypeVar

from core.runtime.context import RuntimeContext


EventKey: TypeAlias = str

EventPayload: TypeAlias = Any

EventMetadata: TypeAlias = dict[str, Any]

ContextT = TypeVar(
    "ContextT",
    bound=RuntimeContext,
)

class DispatchMode(str, Enum):
    """
    Defines how multiple event handlers are executed.
    """

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"


class ProviderMode(str, Enum):
    """
    Defines the lifetime of handler instances
    provided by an EventHandlerProvider.
    """

    TRANSIENT = "transient"

    SINGLETON = "singleton"