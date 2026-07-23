from dataclasses import dataclass

from enums.discovery_type import DiscoveryType
from pydantic import  Field
from runtime.base import BaseResult
from runtime.discovery_descriptor import RequestDescriptor

@dataclass(slots=True)
class DiscoveryRecord:

    type: DiscoveryType

    descriptor: RequestDescriptor


class DiscoveryResult(BaseResult):

    descriptors: list[DiscoveryRecord] = Field(default_factory=list)
