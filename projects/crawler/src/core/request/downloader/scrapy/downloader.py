from __future__ import annotations
from core.extraction.response.resolver import ResponseAdapterResolver
from core.request.downloader.model import DownloaderCapabilities
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
        response_adapter_resolver: ResponseAdapterResolver,
        config: ScrapyDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else ScrapyDownloaderConfig(),
        )
        self._response_adapter_resolver = response_adapter_resolver
        self._executor = executor
        self._bridge = bridge
    @property
    def capabilities(self) -> DownloaderCapabilities:
        return DownloaderCapabilities(
            supports_resumable=True,
            supports_streaming=True,
        )
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

        normalized = self._build_response(
            response,
        )

        adapter = self._response_adapter_resolver.resolve(
            profile=context.descriptor.profile,
            response=normalized,
        )

        return DownloadResult(
            response=adapter,
            success=200 <= response.status < 400,
        )

    async def close(
        self,
    ) -> None:
        await self._executor.close()



    def _build_response(
        self,
        response: Response,
    ) -> ScrapyResponse:

        return ScrapyResponse(
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