from core.extraction.response.base import ResponseAdapter
from core.extraction.response.static import StaticResponseAdapter


class HttpxResponseAdapter(
    StaticResponseAdapter,
):
    def with_body(
        self,
        body: bytes,
    ) -> ResponseAdapter:

        response = self._response.with_body(
            body,
        )

        return HttpxResponseAdapter(
            response,
        )