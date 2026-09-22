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


class DownloadStrategyConfig(BaseConfig):
    chunk_size: int = 8 * 1024 * 1024
    parallel_max_concurrency: int = 4

class ResumeConfig(BaseConfig):

    directory: str = "data/resume"
class ChunkConfig(BaseConfig):

    directory: str = "data/chunk"

class Aria2Config(BaseConfig):
    rpc_url: str = "http://127.0.0.1:6800/jsonrpc"

    rpc_secret: str | None = None

    rpc_timeout: float | None = 30.0

    poll_interval: float = 0.5

    monitor_timeout: float | None = None

    download_directory: str = "data/aria2_downloads"

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


class CrawlConfig(BaseConfig):
    entry_spider: str = "news"
    start_requests: tuple[RequestConfig, ...] = ()

    def create_request(
        self,
        request: CrawlRequest | None = None,
    ) -> CrawlRequest:

        if request is None:
            return CrawlRequest(
                spider=self.entry_spider,
                start_requests=self.start_requests,
            )

        return request.model_copy(
            update={
                "start_requests": (
                    self.start_requests
                    if request.start_requests is None
                    else request.start_requests
                ),
            },
        )

class ApplicationConfig(BaseConfig):
    name: str = "ai-space"
    environment: str = "development"

    resume: ResumeConfig = Field(
        default_factory=ResumeConfig,
    )
    chunk: ChunkConfig = Field(
        default_factory=ChunkConfig,
    )
    download_strategy: DownloadStrategyConfig = Field(
        default_factory=DownloadStrategyConfig,
    )

    aria2: Aria2Config = Field(
        default_factory=Aria2Config,
    )

    runtime: RuntimeConfig = Field(
        default_factory=RuntimeConfig,
    )
    crawl: CrawlConfig = Field(
        default_factory=CrawlConfig,
    )
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

        if self.crawl.entry_spider not in names:
            raise ValueError(
                f"Default spider {self.crawl.entry_spider!r} "
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
    start_requests: tuple[RequestConfig, ...] | None = None
    override: SpiderConfigOverride | None = None

class SpiderConfigOverride(BaseConfig):

    kind: RequestKind | None = None

    profile: RequestProfile | None = None

    middlewares: tuple[
        MiddlewareSpecUnion,
        ...
    ] | None = None

    extraction: ExtractConfigUnion | None = None

    discovery: tuple[
        DiscoveryConfigUnion,
        ...
    ] | None = None



