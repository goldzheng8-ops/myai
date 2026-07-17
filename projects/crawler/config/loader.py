from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from config.config import CrawlerConfig


class ConfigLoader(ABC):

    @abstractmethod
    def load(self) -> Iterable[CrawlerConfig]:
        """加载一个或多个 CrawlerConfig。"""
        ...