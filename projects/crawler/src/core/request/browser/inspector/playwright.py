from core.extraction.response.playwright import PlaywrightResponseAdapter
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState




class PlaywrightBrowserPageInspector(
    BrowserPageInspector,
):

    async def inspect(
        self,
        response: PlaywrightResponseAdapter,
    ) -> BrowserPageState:

        page = response.page

        snapshot = BrowserPageSnapshot(
            url=page.url,
            title=await page.title(),
            content=await page.content(),
            status_code=response.status_code,
        )

        for detector in self._detectors:

            state = await detector.detect(
                page,
                snapshot,
            )

            if state is not None:
                return state

        return BrowserPageState.NORMAL

class PlaywrightBrowserPageInspector(
    BrowserPageInspector,
):

    async def inspect(
        self,
        page: Page,
    ) -> BrowserPageInspection:

        url = page.url

        title = await page.title()

        if await self._is_challenge(page):
            return BrowserPageInspection(
                state=BrowserPageState.CHALLENGE,
                url=url,
                title=title,
                reason="Browser challenge detected.",
            )

        if await self._is_captcha(page):
            return BrowserPageInspection(
                state=BrowserPageState.CAPTCHA,
                url=url,
                title=title,
                reason="CAPTCHA detected.",
            )

        return BrowserPageInspection(
            state=BrowserPageState.NORMAL,
            url=url,
            title=title,
        )