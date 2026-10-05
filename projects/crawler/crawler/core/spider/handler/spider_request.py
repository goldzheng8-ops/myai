from core.request.typing import RequestKind
from core.spider.handler.base import TemplateRequestHandler



class SpiderRequestHandler(
    TemplateRequestHandler,
):
    kinds = frozenset({
        RequestKind.LIST,
        RequestKind.DETAIL,
        RequestKind.API,
    })