from dataclasses import dataclass

from config.config import RequestConfig


@dataclass(slots=True)
class Task:

    id: str

    crawler: str

    request: RequestConfig

    priority: int = 0