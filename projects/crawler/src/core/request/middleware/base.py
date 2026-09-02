from __future__ import annotations
from typing import Generic, TypeVar

from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.plugin import MiddlewarePlugin
MiddlewareConfigT = TypeVar(
    "MiddlewareConfigT",
    bound=MiddlewareConfig,
    contravariant=True,
)

class RequestMiddleware(MiddlewarePlugin, Generic[MiddlewareConfigT]):

    def __init__(
        self,
        config: MiddlewareConfigT,
    ) -> None:
        self._config = (
            config
        )


