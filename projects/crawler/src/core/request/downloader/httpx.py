import asyncio

from core.request.context import RequestContext
from core.request.middleware.proxy.config import ProxyConfig
from core.request.response.model import HttpxResponse
import httpx


from core.request.typing import DownloaderType

from .base import BaseDownloader
from .config import HttpxDownloaderConfig
from .result import DownloadResult


class HttpxDownloader(
    BaseDownloader[HttpxDownloaderConfig],
):
    type = DownloaderType.HTTPX

    def __init__(
        self,
        config: HttpxDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else HttpxDownloaderConfig(),
        )

        self._clients: dict[
            str | None,
            httpx.AsyncClient,
        ] = {}

    async def start(
        self,
    ) -> None:
        return

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        request = self.build_request(
            context,
        )

        client = self._get_client(
            context.descriptor.proxy,
        )

        try:

            response = await client.request(
                method=request.method.value,
                url=request.url,
                headers=dict(request.headers),
                cookies=dict(request.cookies),
                params=dict(request.params),
                content=request.body,
            )

            normalized = HttpxResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                body=response.content,
                cookies=dict(response.cookies),
                encoding=response.encoding,
                reason=response.reason_phrase,
                raw=response,
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

    def _get_client(
        self,
        proxy: ProxyConfig | None,
    ) -> httpx.AsyncClient:

        proxy_url = (
            proxy.as_url()
            if proxy is not None
            else None
        )

        client = self._clients.get(
            proxy_url,
        )

        if client is not None:
            return client

        client = httpx.AsyncClient(
            verify=self.config.verify_ssl,
            follow_redirects=self.config.follow_redirects,
            max_redirects=self.config.max_redirects,
            http2=self.config.http2,
            timeout=self.config.timeout,
            proxy=proxy_url,
        )

        self._clients[proxy_url] = client

        return client

    async def close(
        self,
    ) -> None:

        clients = tuple(
            self._clients.values(),
        )

        self._clients.clear()

        if not clients:
            return

        await asyncio.gather(
            *(
                client.aclose()
                for client in clients
            ),
        )