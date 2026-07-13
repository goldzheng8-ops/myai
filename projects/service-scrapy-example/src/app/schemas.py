from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.models import RetryConfig, SubmissionStatus, TaskStatus


class CrawlTaskRequest(BaseModel):
    spider: str = Field(default="template")
    url: str | None = None
    crawler_config: dict[str, Any] | None = None
    callback_url: str | None = None
    retry_config: RetryConfig | None = None


class CrawlTaskResponse(BaseModel):
    task_id: str
    status: SubmissionStatus
    payload: dict[str, Any]
