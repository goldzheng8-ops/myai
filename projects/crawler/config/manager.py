from __future__ import annotations

from collections.abc import Iterable

from config.loader import ConfigLoader
from config.config import CrawlerConfig
from config.registry import CrawlerConfigRegistry


class ConfigManager:

    def __init__(
        self,
        registry: CrawlerConfigRegistry | None = None,
    ):
        self._registry = registry or CrawlerConfigRegistry()

    def load(
        self,
        loader: ConfigLoader,
    ) -> None:

        for config in loader.load():
            self._registry.register(config)

    def get(
        self,
        name: str,
    ) -> CrawlerConfig:

        return self._registry.get(name)

    def all(
        self,
    ) -> Iterable[CrawlerConfig]:

        return self._registry.all()

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._registry