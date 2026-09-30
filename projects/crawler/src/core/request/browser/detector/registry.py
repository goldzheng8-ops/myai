from core.registry import Registry
from core.request.browser.detector.base import BrowserPageStateDetector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from playwright.async_api import Page
import logging

logger=logging.getLogger(__name__)

class BrowserPageStateDetectorRegistry(
    Registry[
        str,
        BrowserPageStateDetector,
    ],
):

    def ordered(
        self,
    ) -> tuple[BrowserPageStateDetector, ...]:

        return tuple(
            sorted(
                self.values(),
                key=lambda detector: (
                    detector.priority,
                ),
            ),
        )

    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:

        for detector in self.ordered():

            inspection = await detector.detect(
                page,
                snapshot,
            )

            if inspection is not None:
                return inspection

        return None