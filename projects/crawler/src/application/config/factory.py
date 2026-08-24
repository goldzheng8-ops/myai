
from __future__ import annotations

from application.config.model import (
    ApplicationConfig,
    ApplicationFileConfig,
    SpiderDefinition,
    SpiderFileDefinition,
)
from application.spider.registry import SpiderRegistry



class ApplicationConfigFactory:
    """
    Resolves user-facing file configuration
    into application-internal configuration.
    """

    def __init__(
        self,
        spider_registry: SpiderRegistry,
    ) -> None:
        self._spider_registry = spider_registry

    @property
    def spider_registry(
        self,
    ) -> SpiderRegistry:
        return self._spider_registry

    def create(
        self,
        config: ApplicationFileConfig,
    ) -> ApplicationConfig:

        spiders = tuple(
            self._create_spider(
                definition,
            )
            for definition in config.spiders
        )

        return ApplicationConfig(
            name=config.name,
            environment=config.environment,
            runtime=config.runtime,
            spiders=spiders,
        )

    def _create_spider(
        self,
        definition: SpiderFileDefinition,
    ) -> SpiderDefinition:

        spider_type = self._spider_registry.get(
            definition.spider,
        )

        return SpiderDefinition(
            name=definition.name,
            spider_type=spider_type,
            kind=definition.kind,
            profile=definition.profile,
            start_requests=definition.start_requests,
            extraction=definition.extraction,
            discovery=definition.discovery,
            browser=definition.browser,
        )