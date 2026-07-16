from playwright.async_api import async_playwright

from adapters.playwright import PlaywrightResponseAdapter
from downloader.base import DownloaderPlugin
from downloader.result import DownloadResult
from request.context import RequestContext


class PlaywrightDownloader(DownloaderPlugin):

    def __init__(self):
        self.playwright = None
        self.browser = None


    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()

    async def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:

        context = await self.browser.new_context()
        context.set_extra_http_headers(request.headers)
        context.add_cookies(request.cookies)
        page = await context.new_page()
        await page.goto(request.url,timeout=request.timeout * 1000,wait_until="networkidle")
        content = await page.content()
        await context.close()
        return DownloadResult(
            response=PlaywrightResponseAdapter(content),
        )