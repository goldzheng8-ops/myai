from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class HumanVerificationChallengeDetector(
    BrowserPageStateDetector,
):
    """
    Detect generic human-verification challenges.

    Detection is based on semantic challenge markers rather
    than a specific anti-bot vendor.
    """
    priority = 200
    
    _STRONG_MARKERS = (
        "please complete the following challenge",
        "confirm this search was made by a human",
        "please verify that you are human",
        "verify that you are human",
    )

    _SUPPORTING_MARKERS = (
        "challenge",
        "human",
        "verification",
        "verify",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        text = snapshot.body_text.lower()

        if self._has_strong_marker(text):
            return self._inspection(
                snapshot,
                "Strong human-verification marker detected.",
            )

        if self._has_combined_evidence(text):
            return self._inspection(
                snapshot,
                "Combined human-verification markers detected.",
            )

        return None

    @classmethod
    def _has_strong_marker(
        cls,
        text: str,
    ) -> bool:

        return any(
            marker in text
            for marker in cls._STRONG_MARKERS
        )

    @classmethod
    def _has_combined_evidence(
        cls,
        text: str,
    ) -> bool:

        return (
            "challenge" in text
            and (
                "human" in text
                or "verification" in text
                or "verify" in text
            )
        )

    @staticmethod
    def _inspection(
        snapshot: BrowserPageSnapshot,
        reason: str,
    ) -> BrowserPageInspection:

        return BrowserPageInspection(
            state=BrowserPageState.CHALLENGE,
            url=snapshot.url,
            title=snapshot.title,
            reason=reason,
        )