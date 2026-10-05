from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class CloudflareChallengeDetector(
    BrowserPageStateDetector,
):

    priority = 100

    _TITLE_MARKERS = (
        "just a moment",
        "attention required",
    )

    _TEXT_MARKERS = (
        "checking your browser",
        "verify you are human",
        "performing security verification",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        title = snapshot.title.lower()
        text = snapshot.body_text.lower()

        if self._matches_title(title):
            return BrowserPageInspection(
                state=BrowserPageState.CLOUDFLARE_CHALLENGE,
                url=snapshot.url,
                title=snapshot.title,
                reason="Cloudflare challenge page detected.",
            )

        if self._matches_text(text):
            return BrowserPageInspection(
                state=BrowserPageState.CLOUDFLARE_CHALLENGE,
                url=snapshot.url,
                title=snapshot.title,
                reason="Cloudflare challenge text detected.",
            )

        return None

    def _matches_title(
        self,
        title: str,
    ) -> bool:

        return any(
            marker in title
            for marker in self._TITLE_MARKERS
        )

    def _matches_text(
        self,
        text: str,
    ) -> bool:

        return any(
            marker in text
            for marker in self._TEXT_MARKERS
        )