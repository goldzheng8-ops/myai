from __future__ import annotations

from dataclasses import dataclass

from core.request.response import RequestResponse
from core.typing import BaseResult


@dataclass(slots=True)
class DownloadResult(BaseResult):
    """
    Result produced by downloader execution.

    Contains the normalized transport response together
    with the common execution result information inherited
    from BaseResult.
    """

    response: RequestResponse | None = None