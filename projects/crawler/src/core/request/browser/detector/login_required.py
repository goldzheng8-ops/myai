from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class LoginRequiredDetector(
    BrowserPageStateDetector,
):

    _KEYWORDS = (
        "sign in",
        "log in",
        "login",
        "authentication required",
        "please sign in",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageState | None:

        content = snapshot.content.lower()
        title = snapshot.title.lower()

        for keyword in self._KEYWORDS:

            if keyword in title:
                return BrowserPageState.LOGIN_REQUIRED

            if keyword in content:
                return BrowserPageState.LOGIN_REQUIRED

        return None