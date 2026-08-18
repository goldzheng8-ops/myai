from __future__ import annotations
from scrapy.http import Response

from core.request.downloader.scrapy.bridge import ScrapyRequestBridge
from core.request.downloader.scrapy.executor import ScrapyRequestExecutor
from core.request.response.model import ScrapyResponse
from core.request.context import RequestContext
from core.request.typing import DownloaderType
from ..base import BaseDownloader
from ..config import ScrapyDownloaderConfig
from ..result import DownloadResult

class ScrapyDownloader(
    BaseDownloader[ScrapyDownloaderConfig],
):
    type = DownloaderType.SCRAPY

    def __init__(
        self,
        executor: ScrapyRequestExecutor,
        bridge: ScrapyRequestBridge,
        config: ScrapyDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else ScrapyDownloaderConfig(),
        )

        self._executor = executor
        self._bridge = bridge

    @property
    def executor(
        self,
    ) -> ScrapyRequestExecutor:
        return self._executor

    @property
    def bridge(
        self,
    ) -> ScrapyRequestBridge:
        return self._bridge

    async def start(
        self,
    ) -> None:
        await self._executor.start()

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        request = self._bridge.build(
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

    async def close(
        self,
    ) -> None:
        await self._executor.close()

    def _build_result(
        self,
        response: Response,
    ) -> DownloadResult:

        normalized = ScrapyResponse(
            url=response.url,
            status_code=response.status,
            headers=self._build_response_headers(
                response,
            ),
            body=response.body,
            cookies={},
            encoding=None,
            reason=None,
            raw=response,
        )

        return DownloadResult(
            response=normalized,
            success=200 <= response.status < 400,
        )

    @staticmethod
    def _build_response_headers(
        response: Response,
    ) -> dict[str, str]:

        return {
            key.decode("latin-1"): b", ".join(
                values,
            ).decode("latin-1")
            for key, values in response.headers.items()
        }