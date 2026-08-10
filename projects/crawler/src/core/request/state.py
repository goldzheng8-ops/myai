from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class RequestStatus(StrEnum):

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass(slots=True)
class RequestState:
    """
    Runtime execution state of a request.
    """

    status: RequestStatus = RequestStatus.PENDING

    started_at: datetime | None = None

    completed_at: datetime | None = None

    error: Exception | None = None

    def start(
        self,
        *,
        now: datetime | None = None,
    ) -> None:

        self.status = RequestStatus.RUNNING
        self.started_at = (
            now
            if now is not None
            else datetime.now()
        )

    def complete(
        self,
        *,
        now: datetime | None = None,
    ) -> None:

        self.status = RequestStatus.COMPLETED
        self.completed_at = (
            now
            if now is not None
            else datetime.now()
        )

        self.error = None

    def fail(
        self,
        error: Exception,
        *,
        now: datetime | None = None,
    ) -> None:

        self.status = RequestStatus.FAILED
        self.completed_at = (
            now
            if now is not None
            else datetime.now()
        )

        self.error = error