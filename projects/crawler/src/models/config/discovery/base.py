from models.config.selector.base import SelectorConfig
from pydantic import BaseModel,Field
from typing import Any

from models.config.base import BaseConfig
from models.enums.discovery_type import DiscoveryType
from runtime.request_profile import RequestProfile


class DiscoveryConfig(BaseConfig):

    enabled: bool = True
    type: DiscoveryType

class RequestPatch(BaseModel):

    url: str | None = None

    params: dict[str, str] = Field(default_factory=dict)

    body: Any = None


class ApiDiscoveryConfig(DiscoveryConfig):

    patch: RequestPatch

class UrlDiscoveryConfig(DiscoveryConfig):

    profile: RequestProfile

class HtmlDiscoveryConfig(UrlDiscoveryConfig):

    selector: SelectorConfig


class FeedDiscoveryConfig(UrlDiscoveryConfig):
    ...