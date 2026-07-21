from pydantic import BaseModel, Field

from request.context import RequestContext


class DiscoveryResult(BaseModel):

    requests: list[RequestContext] = Field(default_factory=list)

