from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class ServerErrorDetector(
    BrowserPageStateDetector,
):

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageState | None:

        status_code = snapshot.status_code

        if status_code is not None:
            if 500 <= status_code <= 599:
                return BrowserPageState.SERVER_ERROR

        return None