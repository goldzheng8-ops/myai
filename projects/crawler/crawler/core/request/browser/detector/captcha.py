from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page

class CaptchaDetector(
    BrowserPageStateDetector,
):

    priority = 120

    _SELECTORS = (
        "iframe[src*='recaptcha']",
        "iframe[src*='hcaptcha']",
        ".g-recaptcha",
        ".h-captcha",
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
                    state=BrowserPageState.CAPTCHA,
                    url=snapshot.url,
                    title=snapshot.title,
                    reason="CAPTCHA widget detected.",
                )

        return None