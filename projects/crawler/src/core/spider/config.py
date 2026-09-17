from __future__ import annotations

from typing import Annotated, Any, Literal


from core.request.middleware.config import MiddlewareSpecUnion
from pydantic import Field, field_validator

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

    middlewares: tuple[
        MiddlewareSpecUnion,
        ...
    ] = ()
    outputs: tuple[str, ...] = ()
    settings: dict[str, Any] = Field(
        default_factory=dict,
    )

    @field_validator("outputs")
    @classmethod
    def validate_outputs(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError(
                "Spider outputs must be unique."
            )
        return value

class ExtractConSpiderConfig(SpiderConfig):
    extraction: ExtractConfigUnion
    
    discovery: tuple[
        DiscoveryConfigUnion,
        ...
    ] = ()

    template: Literal[SpiderTemplate.EXTRACTION] = (
        SpiderTemplate.EXTRACTION
    )

class DownloadSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.DOWNLOAD] = (
        SpiderTemplate.DOWNLOAD
    )

class PlainSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.PLAIN] = SpiderTemplate.PLAIN





SpiderConfigUnion = Annotated[
    (
        ExtractConSpiderConfig
        | DownloadSpiderConfig
        | PlainSpiderConfig
    ),
    Field(discriminator="template"),
]

