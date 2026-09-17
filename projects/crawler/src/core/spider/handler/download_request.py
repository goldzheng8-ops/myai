
from core.request.typing import RequestKind
from core.spider.handler.base import TemplateRequestHandler



class DownloadRequestHandler(
    TemplateRequestHandler,
):
    kinds = frozenset({
        RequestKind.DOWNLOAD,
    })