from __future__ import annotations

from dataclasses import dataclass

from core.extraction.response import ResponseAdapter
from core.output.model import BinaryStream
from core.typing import BaseResult


@dataclass(slots=True)
class DownloadResult(BaseResult):


    response: ResponseAdapter | None = None
    stream: BinaryStream | None = None

    @property
    def is_streaming(self) -> bool:
        return self.stream is not None