from dataclasses import dataclass, field
from typing import Any

from pydantic import  Field
from runtime.base import BaseResult
from runtime.discovery_descriptor import RequestDescriptor

@dataclass(slots=True)
class DiscoveryRecord:

    descriptor: RequestDescriptor

    metadata: dict[str, Any] = field(default_factory=dict)


class DiscoveryResult(BaseResult):

    descriptors: list[DiscoveryRecord] = Field(default_factory=list)
