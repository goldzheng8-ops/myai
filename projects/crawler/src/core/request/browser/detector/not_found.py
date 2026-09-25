from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class NotFoundDetector(
    BrowserPageStateDetector,
):

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageState | None:

        if snapshot.status_code == 404:
            return BrowserPageState.NOT_FOUND

        content = snapshot.content.lower()
        title = snapshot.title.lower()

        keywords = (
            "404",
            "page not found",
            "not found",
        )

        for keyword in keywords:

            if keyword in title:
                return BrowserPageState.NOT_FOUND

        return None