from core.request.context import RequestContext
import httpx

from core.request.response import RequestResponse
from core.request.typing import DownloaderType

from .base import BaseDownloader
from .config import HTTPXDownloaderConfig
from .result import DownloadResult


class HTTPXDownloader(
    BaseDownloader[HTTPXDownloaderConfig],
):
    type = DownloaderType.HTTPX

    def __init__(
        self,
        config: HTTPXDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else HTTPXDownloaderConfig(),
        )

        self._client: httpx.AsyncClient | None = None

    async def start(
        self,
    ) -> None:

        if self._client is not None:
            return

        self._client = httpx.AsyncClient(
            verify=self.config.verify_ssl,
            follow_redirects=self.config.follow_redirects,
            max_redirects=self.config.max_redirects,
            http2=self.config.http2,
            timeout=self.config.timeout,
        )

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        if self._client is None:
            await self.start()

        assert self._client is not None

        request = self.build_request(
            context,
        )

        try:

            response = await self._client.request(
                method=request.method.value,
                url=request.url,
                headers=dict(request.headers),
                cookies=dict(request.cookies),
                params=dict(request.params),
                content=request.body,
            )

            normalized = RequestResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                body=response.content,
                cookies=dict(response.cookies),
                encoding=response.encoding,
                reason=response.reason_phrase,
            )

            return DownloadResult(
                response=normalized,
                success=response.is_success,
            )

        except Exception as exc:

            return DownloadResult(
                success=False,
                error=exc,
            )

    async def close(
        self,
    ) -> None:

        if self._client is None:
            return

        await self._client.aclose()

        self._client = None