from core.extraction.response.base import ResponseAdapter
from core.extraction.response.static import StaticResponseAdapter


class ScrapyResponseAdapter(
    StaticResponseAdapter,
):
    def with_body(
        self,
        body: bytes,
    ) -> ResponseAdapter:

        response = self._response.with_body(
            body,
        )

        return ScrapyResponseAdapter(
            response,
        )