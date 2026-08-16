from core.extraction.response.httpx import HttpxResponseAdapter
from core.extraction.response.playwright import PlaywrightResponseAdapter
from core.extraction.response.scrapy import ScrapyResponseAdapter

from core.request.response.model import BrowserResponse, HttpxResponse, RequestResponse, ScrapyResponse

from .base import ResponseAdapter


class ResponseAdapterFactory:

    def create(
        self,
        response: RequestResponse,
    ) -> ResponseAdapter:

        if isinstance(response, HttpxResponse):

            return HttpxResponseAdapter(
                response.raw,
            )

        if isinstance(response, ScrapyResponse):

            return ScrapyResponseAdapter(
                response.raw,
            )

        if isinstance(response, BrowserResponse):

            if response.page is None:
                raise RuntimeError(
                    "BrowserResponse does not contain "
                    "a browser page.",
                )

            return PlaywrightResponseAdapter(
                response.page,
            )

        raise TypeError(
            f"Unsupported response type: "
            f"{type(response)!r}",
        )