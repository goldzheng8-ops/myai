from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class LoginRequiredDetector(
    BrowserPageStateDetector,
):

    priority = 2000

    _TEXT_MARKERS = (
        "sign in",
        "log in",
        "login",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        text = snapshot.body_text.lower()

        if any(
            marker in text
            for marker in self._TEXT_MARKERS
        ):

            return BrowserPageInspection(
                state=BrowserPageState.LOGIN_REQUIRED,
                url=snapshot.url,
                title=snapshot.title,
                reason="Login page detected.",
            )

        return None