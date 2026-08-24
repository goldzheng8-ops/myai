from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from core.spider.template import TemplateSpider
from pydantic import  Field

from core.request.descriptor import RequestDescriptor
from core.spider.config import BaseConfig
from core.request.typing import RequestKind
from core.request.profile import RequestProfile

from application.config.base import ApplicationConfigBase


class RuntimeSettings(ApplicationConfigBase):
    concurrency: int = 8
    timeout: float | None = 30.0

@dataclass(frozen=True, slots=True)
class RequestDefinition(ApplicationConfigBase):
    url: str

    method: str = "GET"

    headers: Mapping[str, str] = field(
        default_factory=dict,
    )

    cookies: Mapping[str, str] = field(
        default_factory=dict,
    )

    params: Mapping[str, Any] = field(
        default_factory=dict,
    )

    body: Any | None = None

    meta: Mapping[str, Any] = field(
        default_factory=dict,
    )

@dataclass(frozen=True, slots=True)
class SpiderFileDefinition(ApplicationConfigBase):
    """
    User-facing declarative spider configuration.
    """

    name: str

    spider: str

    kind: RequestKind

    profile: RequestProfile

    start_requests: tuple[
        RequestDefinition,
        ...
    ] = ()

    extraction: Mapping[str, Any] = field(
        default_factory=dict,
    )

    discovery: tuple[
        Mapping[str, Any],
        ...
    ] = ()

    browser: Mapping[str, Any] | None = None

@dataclass(frozen=True, slots=True)
class SpiderDefinition(ApplicationConfigBase):
    """
    Resolved application spider definition.
    """

    name: str

    spider_type: type[
        TemplateSpider[Any]
    ]

    kind: RequestKind

    profile: RequestProfile

    start_requests: tuple[
        RequestDefinition,
        ...
    ] = ()

    extraction: Mapping[str, Any] = field(
        default_factory=dict,
    )

    discovery: tuple[
        Mapping[str, Any],
        ...
    ] = ()

    browser: Mapping[str, Any] | None = None

class ConfigOverride(ApplicationConfigBase):
    start_requests: tuple[RequestDescriptor, ...] | None = None

    kind: RequestKind | None = None

    profile: RequestProfile | None = None

    extraction: dict[str, Any] | None = None

    discovery: tuple[dict[str, Any], ...] | None = None

    browser: dict[str, Any] | None = None


class CrawlRequest(ApplicationConfigBase):
    spider: str

    override: ConfigOverride = Field(
        default_factory=ConfigOverride,
    )


class ApplicationFileConfig(BaseConfig):

    name: str = "ai-space"

    environment: str = "development"

    runtime: RuntimeSettings = Field(
        default_factory=RuntimeSettings,
    )

    spiders: tuple[
        SpiderFileDefinition,
        ...,
    ] = ()

    crawls: tuple[CrawlRequest, ...] = ()


class ApplicationConfig(ApplicationConfigBase):
    """
    Fully resolved application configuration.

    This is the configuration consumed by bootstrap/container.
    """

    name: str = "ai-space"

    environment: str = "development"

    runtime: RuntimeSettings = Field(
        default_factory=RuntimeSettings,
    )

    spiders: tuple[SpiderDefinition, ...] = ()

class ResolvedCrawlConfig(BaseConfig):
    """
    Fully resolved configuration for one crawl job.

    It is produced by ConfigResolver from:
        ApplicationConfig + CrawlRequest.override

    It contains no runtime objects.
    """

    spider: str

    kind: RequestKind

    profile: RequestProfile

    start_requests: tuple[
        RequestDescriptor,
        ...
    ] = ()

    extraction: dict[str, Any] = Field(
        default_factory=dict,
    )

    discovery: tuple[
        dict[str, Any],
        ...
    ] = ()

    browser: dict[str, Any] | None = None