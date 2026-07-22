from urllib.parse import urlparse
from time import perf_counter
from downloader.config.enums import DownloaderType
from playwright.async_api import async_playwright

from adapters.playwright import PlaywrightResponseAdapter
from downloader.base import DownloaderPlugin
from downloader.result import DownloadResult
from request.context import RequestContext


class PlaywrightDownloader(DownloaderPlugin):
    
    type=DownloaderType.PLAYWRIGHT

    def __init__(self):
        self.playwright = None
        self.browser = None


    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def _ensure_started(self) -> None:
        if self.browser is None:
            await self.start()

    async def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:

        await self._ensure_started()
        context = await self.browser.new_context()
        await context.set_extra_http_headers(request.headers)
        if request.cookies:
            await context.add_cookies(
                self._build_cookies(
                    request.url,
                    request.cookies,
                )
            )
        page = await context.new_page()

        start = perf_counter()

        response = await page.goto(request.url, timeout=request.timeout * 1000, wait_until="networkidle")

        elapsed = perf_counter() - start

        return DownloadResult(
            response=PlaywrightResponseAdapter(page),
            elapsed=elapsed,
            status_code=response.status if response else 200,
            headers=response.headers if response else {},
            final_url=page.url,
    )

    def _build_cookies(
        self,
        url: str,
        cookies: dict[str, str],
    ) -> list[dict]:

        domain = urlparse(url).hostname or ""

        return [
            {
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
            }
            for name, value in cookies.items()
        ]