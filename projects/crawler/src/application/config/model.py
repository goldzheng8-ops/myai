from __future__ import annotations

from core.extraction.extractor.config import ExtractConfigUnion
from core.request.config import RequestConfig
from core.request.discovery.config import DiscoveryConfigUnion, RequestProfile
from core.request.middleware.chain_builder import MiddlewareSpecUnion
from core.typing.config import BaseConfig
from pydantic import  Field

from core.spider.config import BrowserConfig, RequestKind, SpiderConfigUnion


from application.config.base import ApplicationConfigBase

class EngineRuntimeConfig(ApplicationConfigBase):
    """
    Runtime configuration of the crawler engine.
    """

    concurrency: int = 8

    timeout: float | None = 30.0


class ThrottleRuntimeConfig(ApplicationConfigBase):
    """
    Runtime configuration of throttling.
    """

    delay: float = 0.0

    concurrency: int | None = None


class RuntimeConfig(ApplicationConfigBase):
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

    spiders: tuple[
        SpiderConfigUnion,
        ...
    ] = ()

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

    browser: BrowserConfig | None = None

