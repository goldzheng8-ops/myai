from dataclasses import dataclass
from datetime import datetime

from .typing import SpiderStatus


@dataclass(slots=True)
class SpiderState:
    """
    Runtime lifecycle state of a spider.
    """

    status: SpiderStatus = SpiderStatus.PENDING

    started_at: datetime | None = None

    completed_at: datetime | None = None

    error: Exception | None = None