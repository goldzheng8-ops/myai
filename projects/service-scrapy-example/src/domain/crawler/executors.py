from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .config import CrawlerConfig


class BaseExecutor(ABC):
    name: str = "base"

    @abstractmethod
    def execute(self, config: CrawlerConfig, task_id: str) -> dict[str, Any]:
        raise NotImplementedError


class ScrapyExecutor(BaseExecutor):
    name = "scrapy"

    def execute(self, config: CrawlerConfig, task_id: str) -> dict[str, Any]:
        return {
            "task_id": task_id,
            "executor": self.name,
            "status": "completed",
            "items": [{"url": config.request.url, "source": "scrapy"}],
        }


class PlaywrightExecutor(BaseExecutor):
    name = "playwright"

    def execute(self, config: CrawlerConfig, task_id: str) -> dict[str, Any]:
        return {
            "task_id": task_id,
            "executor": self.name,
            "status": "completed",
            "items": [{"url": config.request.url, "source": "playwright"}],
        }


class ApiExecutor(BaseExecutor):
    name = "api"

    def execute(self, config: CrawlerConfig, task_id: str) -> dict[str, Any]:
        return {
            "task_id": task_id,
            "executor": self.name,
            "status": "completed",
            "items": [{"url": config.request.url, "source": "api"}],
        }


def select_executor(config: CrawlerConfig) -> BaseExecutor:
    if config.template == "api":
        return ApiExecutor()
    if config.browser.enabled:
        return PlaywrightExecutor()
    return ScrapyExecutor()
