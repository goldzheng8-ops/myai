from __future__ import annotations

from typing import Annotated, Any, Literal


from core.request.browser.interaction.model import BrowserAction
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

class LoginSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.LOGIN] = SpiderTemplate.LOGIN

class FormSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.FORM] = SpiderTemplate.FORM

class UploadFieldConfig(BaseConfig):
    name: str
    path: str
    filename: str | None = None
    content_type: str | None = None

class UploadSpiderConfig(SpiderConfig):
    template: Literal[SpiderTemplate.UPLOAD] = SpiderTemplate.UPLOAD

    files: tuple[UploadFieldConfig, ...] = ()

class SearchSpiderConfig(
    SpiderConfig,
):

    template: Literal[
        SpiderTemplate.SEARCH
    ] = SpiderTemplate.SEARCH


    actions: tuple[BrowserAction, ...] = ()


SpiderConfigUnion = Annotated[
    (
        ExtractConSpiderConfig
        | DownloadSpiderConfig
        | PlainSpiderConfig
        | LoginSpiderConfig
        | SearchSpiderConfig
        | FormSpiderConfig
        | UploadSpiderConfig
    ),
    Field(discriminator="template"),
]
