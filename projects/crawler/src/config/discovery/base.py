from config.selector.base import SelectorConfig
from pydantic import BaseModel,Field
from typing import Any

from core.models.base import BaseConfig
from enums.discovery_type import DiscoveryType
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


class HtmlDiscoveryConfig(DiscoveryConfig):

    selector: SelectorConfig

    profile: RequestProfile
