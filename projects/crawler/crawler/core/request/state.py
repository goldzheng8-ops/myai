from __future__ import annotations
from enum import Enum


class RequestStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"

    def start(self) -> "RequestStatus":
        if self is not RequestStatus.PENDING:
            raise RuntimeError(
                f"Cannot start request from state {self.value!r}.",
            )

        return RequestStatus.RUNNING

    def complete(self) -> "RequestStatus":
        if self is not RequestStatus.RUNNING:
            raise RuntimeError(
                "Cannot complete request from state "
                f"{self.value!r}.",
            )

        return RequestStatus.COMPLETED

    def fail(self) -> "RequestStatus":
        if self is not RequestStatus.RUNNING:
            raise RuntimeError(
                "Cannot fail request from state "
                f"{self.value!r}.",
            )

        return RequestStatus.FAILED

    def skip(self) -> "RequestStatus":
        if self is not RequestStatus.RUNNING:
            raise RuntimeError(
                "Cannot skip request from state "
                f"{self.value!r}.",
            )

        return RequestStatus.SKIPPED

    def cancel(self) -> "RequestStatus":
        if self is not RequestStatus.RUNNING:
            raise RuntimeError(
                "Cannot cancel request from state "
                f"{self.value!r}.",
            )

        return RequestStatus.CANCELLED


class RequestState:

    def __init__(self) -> None:
        self._status = RequestStatus.PENDING
        self._error: BaseException | None = None
        self._reason: str | None = None

    @property
    def status(self) -> RequestStatus:
        return self._status

    @property
    def error(self) -> BaseException | None:
        return self._error

    @property
    def reason(self) -> str | None:
        return self._reason

    @property
    def is_pending(self) -> bool:
        return self._status is RequestStatus.PENDING

    @property
    def is_running(self) -> bool:
        return self._status is RequestStatus.RUNNING

    @property
    def is_completed(self) -> bool:
        return self._status is RequestStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self._status is RequestStatus.FAILED

    @property
    def is_skipped(self) -> bool:
        return self._status is RequestStatus.SKIPPED

    @property
    def is_cancelled(self) -> bool:
        return self._status is RequestStatus.CANCELLED

    def start(self) -> None:
        self._status = self._status.start()

    def complete(self) -> None:
        self._status = self._status.complete()

    def fail(
        self,
        error: BaseException,
    ) -> None:
        self._status = self._status.fail()
        self._error = error

    def skip(
        self,
        reason: str | None = None,
    ) -> None:
        self._status = self._status.skip()
        self._reason = reason

    def cancel(self) -> None:
        self._status = self._status.cancel()