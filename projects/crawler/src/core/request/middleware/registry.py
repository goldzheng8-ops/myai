from __future__ import annotations

from core.registry import Registry
from core.request.middleware import RequestMiddleware
from core.request.middleware.factory import MiddlewareFactory
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.config import MiddlewareConfig



class MiddlewareRegistry(
    Registry[
        MiddlewareType,
        MiddlewareFactory,
    ],
):

    def create(
        self,
        type_: MiddlewareType,
        config: MiddlewareConfig | None = None,
    ) -> RequestMiddleware:
        return self.get(type_)(config)