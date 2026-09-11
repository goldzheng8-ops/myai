from dataclasses import dataclass

from core.typing import BaseResult


@dataclass(slots=True)
class SpiderResult(BaseResult):
    """
    Summary produced by spider execution.
    """

    request_count: int = 0

    item_count: int = 0

