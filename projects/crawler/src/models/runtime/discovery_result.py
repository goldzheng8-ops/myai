from dataclasses import dataclass, field
from typing import Any

from pydantic import  Field
from models.runtime.base import BaseResult
from core.request.descriptor import RequestDescriptor

@dataclass(slots=True)
class DiscoveryRecord:

    descriptor: RequestDescriptor

    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class DiscoveryResult(BaseResult):

    descriptors: list[DiscoveryRecord] = Field(default_factory=list)
