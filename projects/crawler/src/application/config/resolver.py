from __future__ import annotations

from typing import Any

from application.config.model import (
    ApplicationConfig,
    CrawlRequest,
    ResolvedCrawlConfig,
)


class ConfigResolver:
    """
    Resolves application-level defaults and per-crawl overrides
    into a fully resolved crawl configuration.

    This class does not create spiders or runtime objects.
    """

    def resolve(
        self,
        config: ApplicationConfig,
        request: CrawlRequest,
    ) -> ResolvedCrawlConfig:

        spider = self._find_spider(
            config,
            request.spider,
        )

        override = request.override

        return ResolvedCrawlConfig(
            spider=spider.name,
            kind=(
                override.kind
                if override.kind is not None
                else spider.kind
            ),
            profile=(
                override.profile
                if override.profile is not None
                else spider.profile
            ),
            start_requests=(
                override.start_requests
                if override.start_requests is not None
                else spider.start_requests
            ),
            extraction=self._resolve_mapping(
                spider.extraction,
                override.extraction,
            ),
            discovery=(
                override.discovery
                if override.discovery is not None
                else spider.discovery
            ),
            browser=self._resolve_optional_mapping(
                spider.browser,
                override.browser,
            ),
        )

    @staticmethod
    def _find_spider(
        config: ApplicationConfig,
        name: str,
    ):
        for spider in config.spiders:
            if spider.name == name:
                return spider

        raise LookupError(
            f"Unknown spider: {name!r}",
        )

    @staticmethod
    def _resolve_mapping(
        default: dict[str, Any],
        override: dict[str, Any] | None,
    ) -> dict[str, Any]:

        if override is None:
            return dict(default)

        return dict(override)

    @staticmethod
    def _resolve_optional_mapping(
        default: dict[str, Any] | None,
        override: dict[str, Any] | None,
    ) -> dict[str, Any] | None:

        if override is None:
            return (
                None
                if default is None
                else dict(default)
            )

        return dict(override)