from __future__ import annotations
from abc import ABC
from typing import Generic

from core.request.middleware.plugin import MiddlewarePlugin
from .typing import MiddlewareConfigT


class RequestMiddleware(Generic[MiddlewareConfigT],MiddlewarePlugin, ABC):

    def __init__(
        self,
        config: MiddlewareConfigT,
    ) -> None:
        self._config = (
            config
        )


