
from typing import Any

from core.request.typing import HttpMethod
from pydantic import BaseModel, Field


class RequestConfig(BaseModel):
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    cookies: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    method: HttpMethod = HttpMethod.GET
    body: Any = None
    timeout: int = 30
    retry: int = 3
    proxy: str | None = None