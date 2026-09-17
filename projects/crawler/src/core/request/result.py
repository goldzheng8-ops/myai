from dataclasses import dataclass
from typing import Any

from core.extraction.response import ResponseAdapter
from core.typing import BaseResult




@dataclass(slots=True)
class RequestResult(BaseResult):
    """
    Result produced by request execution.
    """

    response: ResponseAdapter

    value: Any = None