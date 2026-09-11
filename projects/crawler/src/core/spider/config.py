from __future__ import annotations

from typing import Annotated, Any, Literal


from core.request.config import RequestConfig
from core.request.middleware.config import MiddlewareSpecUnion
from pydantic import Field

from .typing import SpiderTemplate


from core.request.discovery.config import DiscoveryConfigUnion
from core.extraction.extractor.config import ExtractConfigUnion
from core.request.profile import RequestProfile
from core.request.typing import RequestKind
from core.typing.config import BaseConfig


class SpiderConfig(BaseConfig):
    name: str

    kind: RequestKind

    profile: RequestProfile

    extraction: ExtractConfigUnion
    start_requests: tuple[
        RequestConfig,
        ...
    ] = ()

    middlewares: tuple[
        MiddlewareSpecUnion,
        ...
    ] = ()
    settings: dict[str, Any] = Field(
        default_factory=dict,
    )
    outputs: tuple[str, ...] 

class DiscoverySpiderConfig(SpiderConfig):
    discovery: tuple[
        DiscoveryConfigUnion,
        ...
    ] = ()


class ListSpiderConfig(DiscoverySpiderConfig):
    template: Literal[SpiderTemplate.LIST] = SpiderTemplate.LIST




class DetailSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.DETAIL] = (
        SpiderTemplate.DETAIL
    )




class ApiSpiderConfig(DiscoverySpiderConfig):
    template: Literal[SpiderTemplate.API] = SpiderTemplate.API




class BrowserSpiderConfig(DiscoverySpiderConfig):
    template: Literal[SpiderTemplate.BROWSER] = (
        SpiderTemplate.BROWSER
    )




SpiderConfigUnion = Annotated[
    (
        ListSpiderConfig
        | DetailSpiderConfig
        | ApiSpiderConfig
        | BrowserSpiderConfig
    ),
    Field(discriminator="template"),
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
