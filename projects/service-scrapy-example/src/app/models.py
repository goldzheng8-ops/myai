from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SubmissionStatus(str, Enum):
    ACCEPTED = "accepted"


class RetryConfig(BaseModel):
    enabled: bool = True
    retries: int = 3
    delay_seconds: float = 1.0
    timeout_seconds: float = 10.0


class TaskRecord(BaseModel):
    task_id: str
    status: TaskStatus = TaskStatus.QUEUED
    spider: str
    url: str | None = None
    callback_url: str | None = None
    result: dict[str, Any] | None = None
    callback_error: str | None = None
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
