from core.request.typing import RequestKind
from core.spider.handler.base import TemplateRequestHandler


class SearchRequestHandler(
    TemplateRequestHandler,
):
    kinds = frozenset({
        RequestKind.SEARCH,
    })