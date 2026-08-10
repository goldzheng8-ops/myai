from dataclasses import dataclass
from typing import Any

from core.typing import BaseResult

from .response import RequestResponse


@dataclass(slots=True)
class RequestResult(BaseResult):
    """
    Result produced by request execution.
    """

    response: RequestResponse | None = None

    value: Any = None