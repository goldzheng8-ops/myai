from dataclasses import dataclass, field
from typing import Generic

from core.runtime import RuntimeContext


from .result import SpiderResult
from .state import SpiderState
from .typing import ConfigT




@dataclass(slots=True)
class SpiderContext(
    Generic[ConfigT],
):
    """
    Runtime context of a single spider execution.
    """

    config: ConfigT

    runtime: RuntimeContext = field(
        default_factory=RuntimeContext,
    )

    state: SpiderState = field(
        default_factory=SpiderState,
    )

    result: SpiderResult | None = None