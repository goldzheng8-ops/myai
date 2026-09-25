from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class ChallengeDetector(
    BrowserPageStateDetector,
):

    _KEYWORDS = (
        "captcha",
        "challenge",
        "verify you are human",
        "human verification",
        "are you a human",
        "unusual traffic",
        "automated requests",
        "bot detection",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageState | None:

        content = snapshot.content.lower()
        title = snapshot.title.lower()

        for keyword in self._KEYWORDS:

            if keyword in content:
                return BrowserPageState.CHALLENGE

            if keyword in title:
                return BrowserPageState.CHALLENGE

        return None