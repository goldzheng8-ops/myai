from __future__ import annotations
from typing import Self

from core.extraction.extractor.config import ExtractConfigUnion
from core.output.config import OutputConfigUnion
from core.request.config import RequestConfig
from core.request.discovery.config import DiscoveryConfigUnion
from core.request.middleware.auth.config import AuthProviderConfigUnion
from core.request.middleware.proxy.config import ProxyProviderConfigUnion
from core.request.middleware.retry.config import RetryPolicyConfig
from core.request.middleware.robots.config import RobotsPolicyConfig
from core.request.middleware.user_agent.config import UserAgentProviderConfigUnion
from core.request.profile import RequestProfile
from core.request.middleware.chain_builder import MiddlewareSpecUnion
from core.typing.config import BaseConfig
from pydantic import  Field, model_validator

from core.spider.config import  RequestKind, SpiderConfigUnion

class EngineRuntimeConfig(BaseConfig):
    """
    Runtime configuration of the crawler engine.
    """
    concurrency: int = Field(default=8, gt=0)

    timeout: float | None = Field(
        default=30.0,
        gt=0,
    )

class ThrottleRuntimeConfig(BaseConfig):
    """
    Runtime configuration of throttling.
    """

    delay: float = Field(
        default=0.0,
        ge=0,
    )

    concurrency: int | None = Field(
        default=None,
        gt=0,
    )


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

    robots_policy: RobotsPolicyConfig = Field(
        default_factory=RobotsPolicyConfig,
    )

    retry_policy: RetryPolicyConfig = Field(
        default_factory=RetryPolicyConfig,
    )



class ApplicationConfig(BaseConfig):
    name: str = "ai-space"
    environment: str = "development"

    runtime: RuntimeConfig = Field(
        default_factory=RuntimeConfig,
    )
    default_spider: str = "news"
    proxies: tuple[ProxyProviderConfigUnion, ...] = ()
    user_agents: tuple[UserAgentProviderConfigUnion, ...] = ()
    auth_providers: tuple[AuthProviderConfigUnion, ...] = ()
    output_sinks: tuple[OutputConfigUnion, ...] = ()

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
        output_names = {
            output.name
            for output in self.output_sinks
        }

        for spider in self.spiders:
            for output_name in spider.outputs:
                if output_name not in output_names:
                    raise ValueError(
                        f"Spider {spider.name!r} references "
                        f"unknown output sink {output_name!r}."
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



