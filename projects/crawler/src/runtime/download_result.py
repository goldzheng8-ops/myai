from dataclasses import dataclass

from adapters.base import ResponseAdapter
from runtime.base import BaseResult


@dataclass(slots=True)
class DownloadResult(BaseResult):

    response: ResponseAdapter

    status_code: int

    final_url: str

    headers: dict[str, str]

    retry_count: int = 0

    from_cache: bool = False