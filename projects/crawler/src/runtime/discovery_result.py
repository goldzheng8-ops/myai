from pydantic import  Field
from runtime.base import BaseResult
from runtime.discovery_delta import RequestDelta


class DiscoveryResult(BaseResult):

    deltas: list[RequestDelta] = Field(default_factory=list)
