from __future__ import annotations

from typing import Protocol
from collections.abc import Mapping

from scrapy import Request
from scrapy.http import Response

from core.request.context import RequestContext
from core.request.response import RequestResponse
from core.request.typing import DownloaderType

from .base import BaseDownloader
from .config import ScrapyDownloaderConfig
from .result import DownloadResult


class ScrapyRequestExecutor(Protocol):

    async def execute(
        self,
        request: Request,
    ) -> Response:
        ...


class ScrapyDownloader(
    BaseDownloader[ScrapyDownloaderConfig],
):
    type = DownloaderType.SCRAPY

    def __init__(
        self,
        executor: ScrapyRequestExecutor,
        config: ScrapyDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else ScrapyDownloaderConfig(),
        )

        self._executor = executor

    @property
    def executor(
        self,
    ) -> ScrapyRequestExecutor:

        return self._executor

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        request = self._build_scrapy_request(
            context,
        )

        try:

            response = await self._executor.execute(
                request,
            )

        except Exception as exc:

            return DownloadResult(
                error=exc,
                success=False,
            )

        return self._build_result(
            response,
        )

    def _build_scrapy_request(
        self,
        context: RequestContext,
    ) -> Request:

        request = self.build_request(
            context,
        )

        return Request(
            url=request.url,
            method=request.method.value,
            headers=self._build_scrapy_headers(
                request.headers,
            ),
            cookies=self._build_scrapy_cookies(
                request.cookies,
            ),
            body=request.body,
            cb_kwargs={
                "request_context": context,
            },
        )

    def _build_scrapy_headers(
        self,
        headers: Mapping[str, str],
    ) -> dict[str, str]:

        return {
            str(name): str(value)
            for name, value in headers.items()
        }

    def _build_scrapy_cookies(
        self,
        cookies: Mapping[str, str],
    ) -> dict[str | bytes, str | bytes]:

        return {
            name: value
            for name, value in cookies.items()
        }

    def _build_result(
        self,
        response: Response,
    ) -> DownloadResult:

        normalized = RequestResponse(
            url=response.url,
            status_code=response.status,
            headers=self._build_response_headers(
                response,
            ),
            body=response.body,
            cookies={},
            encoding=None,
            reason=None,
        )

        return DownloadResult(
            response=normalized,
            success=200 <= response.status < 400,
        )

    def _build_response_headers(
        self,
        response: Response,
    ) -> dict[str, str]:

        return {
            key.decode("latin-1"): b", ".join(
                values,
            ).decode("latin-1")
            for key, values in response.headers.items()
        }