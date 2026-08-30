from __future__ import annotations
from typing import Any

from core.registry import Registry
from core.request.middleware import RequestMiddleware
from core.request.middleware.factory import MiddlewareFactory
from core.request.middleware.typing import MiddlewareType
from core.request.middleware.config import MiddlewareConfig



class MiddlewareRegistry(
    Registry[
        MiddlewareType,
        MiddlewareFactory[Any],
    ],
):

    def create(
        self,
        type_: MiddlewareType,
        config: MiddlewareConfig,
    ) -> RequestMiddleware[Any]:
        return self.get(type_)(config)