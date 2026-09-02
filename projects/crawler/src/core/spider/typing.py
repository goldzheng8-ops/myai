# core/spider/typing.py
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from core.spider.config import SpiderConfig


class SpiderTemplate(str, Enum):
    LIST = "list"
    DETAIL = "detail"
    API = "api"
    BROWSER = "browser"


class SpiderStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

ConfigT = TypeVar(
    "ConfigT",
    bound="SpiderConfig",
    covariant=True,
)