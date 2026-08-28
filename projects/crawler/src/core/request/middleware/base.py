from __future__ import annotations
from abc import ABC



from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.plugin import MiddlewarePlugin







class RequestMiddleware(MiddlewarePlugin, ABC):

    def __init__(
        self,
        config: MiddlewareConfig | None = None,
    ) -> None:
        self._config = (
            config
            if config is not None
            else MiddlewareConfig()
        )

    @property
    def config(self) -> MiddlewareConfig:
        return self._config
