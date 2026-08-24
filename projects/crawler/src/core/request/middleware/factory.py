
from typing import Protocol

from core.request.middleware import RequestMiddleware
from core.request.middleware.config import MiddlewareConfig


class MiddlewareFactory(Protocol):
    def __call__(
        self,
        config: MiddlewareConfig | None = None,
    ) -> RequestMiddleware:
        ...