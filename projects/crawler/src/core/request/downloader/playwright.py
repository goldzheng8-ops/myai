from __future__ import annotations

from core.extraction.response.resolver import ResponseAdapterResolver
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.request.context import RequestContext
from core.request.downloader.model import DownloaderCapabilities
from core.request.response.model import BrowserResponse
from playwright.async_api import (
    BrowserContext,
    Page,
    Response,
)

from core.request.typing import DownloaderType

from .base import BaseDownloader
from .config import PlaywrightDownloaderConfig
from .request import DownloadRequest
from .result import DownloadResult

class PlaywrightDownloader(
    BaseDownloader[PlaywrightDownloaderConfig],
):

    type = DownloaderType.PLAYWRIGHT

    def __init__(
        self,
        response_adapter_resolver: ResponseAdapterResolver,
        browser_runtime: BrowserRuntimeManager,
        config: PlaywrightDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else PlaywrightDownloaderConfig(),
        )

        self._response_adapter_resolver = (
            response_adapter_resolver
        )

        self._browser_runtime = browser_runtime

    @property
    def capabilities(
        self,
    ) -> DownloaderCapabilities:

        return DownloaderCapabilities(
            supports_resumable=False,
            supports_streaming=False,
            supports_range=False,
        )

    async def start(self) -> None:

        await self._browser_runtime.start()

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        try:

            session_id = self._require_session_id(
                context,
            )

            session = (
                await self._browser_runtime.get_session(
                    session_id=session_id,
                    proxy=context.descriptor.proxy,
                )
            )

            request = self.build_request(
                context,
            )

            async with session.lock:

                response = await self._navigate(
                    session.page,
                    request,
                )

                if response is None:
                    return DownloadResult(
                        success=False,
                    )

                normalized = (
                    await self._build_response(
                        response=response,
                        page=session.page,
                        browser_context=session.context,
                    )
                )

            adapter = (
                self._response_adapter_resolver.resolve(
                    profile=context.descriptor.profile,
                    response=normalized,
                )
            )

            return DownloadResult(
                response=adapter,
                success=(
                    200
                    <= normalized.status_code
                    < 400
                ),
            )

        except Exception as exc:

            return DownloadResult(
                success=False,
                error=exc,
            )

    async def close(self) -> None:
        # BrowserRuntimeManager is owned by
        # LifecycleManager.
        return

    def _timeout_ms(
        self,
    ) -> float | None:

        if self.config.timeout is None:
            return None

        return self.config.timeout * 1000

    async def _navigate(
        self,
        page: Page,
        request: DownloadRequest,
    ) -> Response | None:

        return await page.goto(
            request.url,
            wait_until=self.config.wait_until,
            timeout=self._timeout_ms(),
        )

    async def _build_response(
        self,
        response: Response,
        page: Page,
        browser_context: BrowserContext
    ) -> BrowserResponse:

        body = await response.body()

        return BrowserResponse(
            url=response.url,
            status_code=response.status,
            headers=await response.all_headers(),
            body=body,
            encoding=None,
            reason=None,
            page=page,
            browser_context=browser_context
        )
    def _require_session_id(
        self,
        context: RequestContext,
    ) -> str:
        session_id= context.session_id
        if session_id is None:
            raise RuntimeError("require session id")
        return session_id

            
