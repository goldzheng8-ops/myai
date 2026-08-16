from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, Literal


from core.request.config import RequestConfig
from pydantic import BaseModel, ConfigDict, Field

from .typing import SpiderTemplate


from core.request.discovery.config import DiscoveryConfig
from core.extraction.extractor.config import ExtractConfig
from core.request.profile import RequestProfile
from core.request.typing import RequestKind



class SpiderConfig(BaseModel):
    """
    Common static configuration of a spider.
    """

    model_config = ConfigDict(
        frozen=True,
    )

    name: str

    kind: RequestKind

    profile: RequestProfile

    template: SpiderTemplate

    start_requests: tuple[
        RequestConfig,
        ...,
    ] = ()

    settings: dict[str, Any] = Field(
        default_factory=dict,
    )

class ListSpiderConfig(SpiderConfig):

    extraction: ExtractConfig

    discovery: tuple[
        DiscoveryConfig,
        ...,
    ] = ()

class DetailSpiderConfig(SpiderConfig):

    extraction: ExtractConfig

class ApiSpiderConfig(SpiderConfig):

    extraction: ExtractConfig

    discovery: tuple[
        DiscoveryConfig,
        ...,
    ] = ()

class BrowserSpiderConfig(SpiderConfig):

    extraction: ExtractConfig

    discovery: tuple[DiscoveryConfig, ...] = ()

    browser: BrowserConfig

SpiderConfigUnion = Annotated[
    (
        ListSpiderConfig
        | DetailSpiderConfig
        | ApiSpiderConfig
        | BrowserSpiderConfig
    ),
    Field(
        discriminator="template",
    ),
]

BrowserType = Literal[
    "chromium",
    "firefox",
    "webkit",
]

WaitUntil = Literal[
    "commit",
    "domcontentloaded",
    "load",
    "networkidle",
]


@dataclass(frozen=True, slots=True)
class BrowserConfig:
    """
    Browser execution configuration for a browser spider.
    """

    browser: BrowserType = "chromium"

    headless: bool = True

    wait_until: WaitUntil = "load"

    timeout: float | None = 30.0

    viewport_width: int = 1280

    viewport_height: int = 720

    user_agent: str | None = None

    javascript: bool = True