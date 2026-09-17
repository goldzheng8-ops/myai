from __future__ import annotations

from dataclasses import dataclass

from core.extraction.response import ResponseAdapter
from core.typing import BaseResult


@dataclass(slots=True)
class DownloadResult(BaseResult):


    response: ResponseAdapter | None = None