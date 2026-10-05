from core.extraction.response.aria2 import Aria2ResponseAdapter
from core.extraction.response.httpx import HttpxResponseAdapter
from core.extraction.response.playwright import PlaywrightResponseAdapter
from core.extraction.response.scrapy import ScrapyResponseAdapter
from core.request.profile import RequestProfile
from core.request.typing import DownloaderType
from core.request.response.model import  RequestResponse

from .base import ResponseAdapter


class ResponseAdapterResolver:

    def resolve(
        self,
        *,
        profile: RequestProfile,
        response: RequestResponse,
    ) -> ResponseAdapter:

        downloader = profile.downloader.type

        if downloader == DownloaderType.HTTPX:
            return HttpxResponseAdapter(response)

        if downloader == DownloaderType.SCRAPY:
            return ScrapyResponseAdapter(response)

        if downloader == DownloaderType.PLAYWRIGHT:
            return PlaywrightResponseAdapter(response)

        if downloader == DownloaderType.ARIA2:
            return Aria2ResponseAdapter(response)

        raise TypeError(
            "Unsupported downloader type: "
            f"{downloader!r}",
        )