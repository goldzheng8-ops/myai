from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class AccessDeniedDetector(
    BrowserPageStateDetector,
):

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageState | None:

        if snapshot.status_code in {
            401,
            403,
        }:
            return BrowserPageState.ACCESS_DENIED

        content = snapshot.content.lower()
        title = snapshot.title.lower()

        keywords = (
            "access denied",
            "forbidden",
            "permission denied",
        )

        for keyword in keywords:

            if keyword in title:
                return BrowserPageState.ACCESS_DENIED

            if keyword in content:
                return BrowserPageState.ACCESS_DENIED

        return None