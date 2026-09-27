from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class NormalPageDetector(
    BrowserPageStateDetector,
):

    priority = 10000

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        return BrowserPageInspection(
            state=BrowserPageState.NORMAL,
            url=snapshot.url,
            title=snapshot.title,
        )