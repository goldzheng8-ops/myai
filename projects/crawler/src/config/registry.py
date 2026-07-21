from __future__ import annotations

from collections.abc import Iterable

from config.config import CrawlerConfig


class CrawlerConfigRegistry:

    def __init__(self):
        self._configs: dict[str, CrawlerConfig] = {}

    def register(self, config: CrawlerConfig) -> None:
        if config.name in self._configs:
            raise ValueError(
                f"Crawler '{config.name}' already registered."
            )

        self._configs[config.name] = config

    def get(self, name: str) -> CrawlerConfig:
        try:
            return self._configs[name]
        except KeyError as exc:
            raise KeyError(
                f"Crawler '{name}' not found."
            ) from exc

    def all(self) -> Iterable[CrawlerConfig]:
        return self._configs.values()

    def __contains__(self, name: str) -> bool:
        return name in self._configs