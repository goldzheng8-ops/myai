from dataclasses import dataclass, field
from typing import Any

from adapters.base import ResponseAdapter


@dataclass(slots=True)
class DownloadResult:

    response: ResponseAdapter

    status_code: int

    final_url: str

    elapsed: float

    headers: dict[str, str]

    retry_count: int = 0

    from_cache: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)