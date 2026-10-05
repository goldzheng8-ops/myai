from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class TurnstileChallengeDetector(
    BrowserPageStateDetector,
):

    priority = 110

    _SELECTORS = (
        "iframe[src*='challenges.cloudflare.com']",
        "iframe[src*='turnstile']",
        "[class*='cf-turnstile']",
        "[data-sitekey]",
    )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        for selector in self._SELECTORS:

            if await page.locator(
                selector,
            ).count() > 0:

                return BrowserPageInspection(
                    state=BrowserPageState.TURNSTILE_CHALLENGE,
                    url=snapshot.url,
                    title=snapshot.title,
                    reason=(
                        "Cloudflare Turnstile "
                        "challenge detected."
                    ),
                )

        return None