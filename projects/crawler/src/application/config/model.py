from __future__ import annotations
from typing import Self

from core.extraction.extractor.config import ExtractConfigUnion
from core.request.config import RequestConfig
from core.request.discovery.config import DiscoveryConfigUnion
from core.request.profile import RequestProfile
from core.request.middleware.chain_builder import MiddlewareSpecUnion
from core.typing.config import BaseConfig
from pydantic import  Field, model_validator

from core.spider.config import  RequestKind, SpiderConfigUnion

class EngineRuntimeConfig(BaseConfig):
    """
    Runtime configuration of the crawler engine.
    """

    concurrency: int = 8

    timeout: float | None = 30.0


class ThrottleRuntimeConfig(BaseConfig):
    """
    Runtime configuration of throttling.
    """

    delay: float = 0.0

    concurrency: int | None = None


class RuntimeConfig(BaseConfig):
    """
    Application runtime configuration.
    """

    engine: EngineRuntimeConfig = Field(
        default_factory=EngineRuntimeConfig,
    )

    throttle: ThrottleRuntimeConfig = Field(
        default_factory=ThrottleRuntimeConfig,
    )

class ApplicationConfig(BaseConfig):
    name: str = "ai-space"
    environment: str = "development"

    runtime: RuntimeConfig = Field(
        default_factory=RuntimeConfig,
    )
    default_spider: str = "news"
    spiders: tuple[
        SpiderConfigUnion,
        ...
    ] = ()
    @model_validator(mode="after")
    def validate_default_spider(self) -> Self:
        names = {
            spider.name
            for spider in self.spiders
        }

        if self.default_spider not in names:
            raise ValueError(
                f"Default spider {self.default_spider!r} "
                "is not registered."
            )

        return self
class CrawlRequest(BaseConfig):
    spider: str

    override: SpiderConfigOverride | None = None

class SpiderConfigOverride(BaseConfig):

    kind: RequestKind | None = None

    profile: RequestProfile | None = None

    start_requests: tuple[
        RequestConfig,
        ...
    ] | None = None

    middlewares: tuple[
        MiddlewareSpecUnion,
        ...
    ] | None = None

    extraction: ExtractConfigUnion | None = None

    discovery: tuple[
        DiscoveryConfigUnion,
        ...
    ] | None = None



