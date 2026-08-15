from dataclasses import dataclass, field
from typing import Any

from core.request.descriptor import RequestDescriptor
from core.typing import BaseResult


@dataclass(slots=True)
class SpiderResult(BaseResult):
    """
    Result produced by spider execution.
    """

    data: Any = None

    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )

    items: list[Any] = field(
        default_factory=list,
    )

# from __future__ import annotations

# from dataclasses import dataclass, field
# from typing import Any

# from core.typing import BaseResult

# from .typing import SpiderStatus


# @dataclass(slots=True)
# class SpiderResult(BaseResult):
#     """
#     Result produced by a complete spider execution.
#     """

#     status: SpiderStatus = SpiderStatus.COMPLETED

#     data: Any = None

#     requests: int = 0

#     succeeded_requests: int = 0

#     failed_requests: int = 0

#     extracted: int = 0

#     metadata: dict[str, Any] = field(
#         default_factory=dict,
#     )