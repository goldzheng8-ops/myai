from __future__ import annotations

from core.request.context import RequestContext
from core.request.response.model import BrowserResponse
from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    Playwright,
    ProxySettings,
    Response,
    async_playwright,
)

from core.request.response import RequestResponse
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
        config: PlaywrightDownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else PlaywrightDownloaderConfig(),
        )

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def start(
        self,
    ) -> None:

        if self._browser is not None:
            return

        self._playwright = (
            await async_playwright().start()
        )

        browser_type = self._get_browser_type()

        self._browser = await browser_type.launch(
            headless=self.config.headless,
        )

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        if self._browser is None:
            await self.start()

        assert self._browser is not None

        request = self.build_request(
            context,
        )

        browser_context = (
            await self._browser.new_context(
                locale=self.config.locale,
                user_agent=self.config.user_agent,
                java_script_enabled=self.config.javascript,
                proxy=self._build_proxy(context),
            )
        )

        try:

            page = await browser_context.new_page()

            response = await self._navigate(
                page,
                request,
            )

            if response is None:
                return DownloadResult(
                    success=False,
                )

            normalized = await self._build_response(
                response,
                page,
                browser_context,
            )

            return DownloadResult(
                response=normalized,
                success=200 <= normalized.status_code < 400,
            )

        except Exception as exc:

            await browser_context.close()

            return DownloadResult(
                success=False,
                error=exc,
            )

    def _get_browser_type(
        self,
    ) -> BrowserType:

        assert self._playwright is not None

        if self.config.browser == "chromium":
            return self._playwright.chromium

        if self.config.browser == "firefox":
            return self._playwright.firefox

        return self._playwright.webkit


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
    ) -> RequestResponse:

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

    async def close(
        self,
    ) -> None:

        if self._browser is not None:
            await self._browser.close()
            self._browser = None

        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None
            
    def _build_proxy(
        self,
        context: RequestContext,
    ) -> ProxySettings | None:

        proxy = context.descriptor.proxy

        if proxy is None:
            return None

        result: ProxySettings = {
            "server": proxy.url,
        }

        if proxy.username is not None:
            result["username"] = proxy.username

        if proxy.password is not None:
            result["password"] = proxy.password

        return result