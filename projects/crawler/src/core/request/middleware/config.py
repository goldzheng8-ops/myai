
from dataclasses import dataclass

from core.request.middleware.typing import MiddlewareType


@dataclass(frozen=True, slots=True)
class MiddlewareConfig:

    priority: int = 0
    enabled: bool = True

class MiddlewareSpec:
    type: MiddlewareType
    config: MiddlewareConfig