

from dataclasses import dataclass

from config.config import Any
from downloader.result import DownloadResult
from request.context import RequestContext


@dataclass(slots=True)
class RunResult:

    context: RequestContext

    download: DownloadResult

    data: dict[str, Any]