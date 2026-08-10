

from dataclasses import dataclass

from models.config.config import Any
from core.request.downloader.result import DownloadResult
from request.context import RequestContext


@dataclass(slots=True)
class RunResult:

    context: RequestContext

    download: DownloadResult

    data: dict[str, Any]