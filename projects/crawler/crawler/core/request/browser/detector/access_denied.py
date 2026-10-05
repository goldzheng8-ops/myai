from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class AccessDeniedDetector(
    BrowserPageStateDetector,
):

    priority = 3000

    _TITLE_MARKERS = (
        "access denied",
        "forbidden",
    )

    _TEXT_MARKERS = (
        "access denied",
        "forbidden",
        "you don't have permission",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        title = snapshot.title.lower()
        text = snapshot.body_text.lower()

        if any(
            marker in title
            for marker in self._TITLE_MARKERS
        ):
            return BrowserPageInspection(
                state=BrowserPageState.ACCESS_DENIED,
                url=snapshot.url,
                title=snapshot.title,
                reason="Access denied page detected.",
            )

        if any(
            marker in text
            for marker in self._TEXT_MARKERS
        ):
            return BrowserPageInspection(
                state=BrowserPageState.ACCESS_DENIED,
                url=snapshot.url,
                title=snapshot.title,
                reason="Access denied page detected.",
            )

        return None