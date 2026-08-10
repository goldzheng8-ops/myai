from dataclasses import dataclass

from core.typing import BaseResult
from core.request.response import RequestResponse


@dataclass(slots=True)
class DownloadResult(BaseResult):
    """
    Result produced by downloader execution.
    """

    response: RequestResponse | None = None