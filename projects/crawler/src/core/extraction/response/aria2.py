from __future__ import annotations
from typing import Any, Mapping

from core.extraction.response.base import ResponseAdapter
from core.request.response.model import (
    RequestResponse,
)


class Aria2ResponseAdapter(
    ResponseAdapter,
):

    def __init__(
        self,
        response: RequestResponse,
    ) -> None:

        super().__init__()

        self._response = response

    @property
    def response(
        self,
    ) -> RequestResponse:

        return self._response

    @property
    def url(
        self,
    ) -> str:

        return self._response.url

    @property
    def status_code(
        self,
    ) -> int:

        return self._response.status_code

    @property
    def headers(
        self,
    ) -> Mapping[str, str]:

        return self._response.headers

    @property
    def body(
        self,
    ) -> bytes:

        return self._response.body

    @property
    def encoding(
        self,
    ) -> str | None:

        return self._response.encoding

    def with_body(
        self,
        body: bytes,
    ) -> Aria2ResponseAdapter:

        response = self._response.with_body(
            body,
        )

        return Aria2ResponseAdapter(
            response,
        )

    async def content(
        self,
    ) -> str:

        return self._response.text

    async def json(
        self,
    ) -> Any:

        import json

        return json.loads(
            self._response.body,
        )

    async def close(
        self,
    ) -> None:

        return None