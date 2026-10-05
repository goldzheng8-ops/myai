from core.registry import Registry
from core.request.typing import RequestKind
from core.spider.handler.base import RequestKindHandler


class RequestKindHandlerRegistry(
    Registry[
        RequestKind,
        RequestKindHandler,
    ],
):
    pass