from __future__ import annotations
from abc import ABC



from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.plugin import MiddlewarePlugin







class RequestMiddleware(MiddlewarePlugin,ABC):
    """
    Base class for request middleware.

    Middleware may execute logic before and/or after
    the next middleware in the chain.
    """


    def __init__(
        self,
        config: MiddlewareConfig,
    ) -> None:

        self._config = config

    @property
    def config(
        self,
    ) -> MiddlewareConfig:

        return self._config
