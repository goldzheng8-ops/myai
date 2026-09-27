from __future__ import annotations

from core.extraction.response.resolver import ResponseAdapterResolver
from core.request.browser.cookie_sink import SessionCookieSink
from core.request.browser.runtime_manager import BrowserRuntimeManager
from core.request.context import RequestContext

from core.request.downloader.extractor.playwright import PlaywrightCookieExtractor
from core.request.downloader.model import DownloaderCapabilities
from core.request.middleware.session.middleware import SESSION_RUNTIME_KEY
from core.request.middleware.session.model import Session
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
        cookie_extractor: PlaywrightCookieExtractor,        
        config: PlaywrightDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else PlaywrightDownloaderConfig(),
            response_adapter_resolver,
        )
        self._browser_runtime = browser_runtime
        self._cookie_extractor=cookie_extractor
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

            session_id = (
                self._require_session_id(
                    context,
                )
            )

            framework_session = (
                self._get_framework_session(
                    context,
                )
            )

            cookie_sink = SessionCookieSink(
                framework_session,
            )

            browser_session = (
                await self._browser_runtime.get_session(
                    session_id=session_id,
                    proxy=context.descriptor.proxy,
                    cookie_sink=cookie_sink,
                )
            )

            request = self.build_request(
                context,
            )

            async with browser_session.lock:

                await self._browser_runtime.apply_cookies(
                    session=browser_session,
                    cookies=context.descriptor.cookies,
                    url=context.descriptor.url,
                )

                response = await self._navigate(
                    browser_session.page,
                    request,
                )

                if response is None:
                    return DownloadResult(
                        success=False,
                    )

                normalized = (
                    await self._build_response(
                        response=response,
                        page=browser_session.page,
                        browser_context=(
                            browser_session.context
                        ),
                    )
                )

            return self._set_result(
                context,
                normalized,
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
        cookies=await self._cookie_extractor.extract(response)
        return BrowserResponse(
            url=response.url,
            status_code=response.status,
            headers=await response.all_headers(),
            body=body,
            cookies=cookies,
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
            raise RuntimeError(
                "Playwright request requires a session_id.",
            )
        return session_id
    def _get_framework_session(
        self,
        context: RequestContext,       
    ) -> Session:
        session = context.runtime.get(
            SESSION_RUNTIME_KEY,
        )

        if not isinstance(session, Session):
            raise RuntimeError(
                "Playwright request requires an active Session.",
            )

        return session