from pydantic import BaseModel, Field

from request.context import RequestContext


class PaginationResult(BaseModel):

    requests: list[RequestContext] = Field(default_factory=list)

    has_next: bool = False