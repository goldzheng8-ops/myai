from core.request.browser.stabilizer.base import BrowserPageStabilizer
from playwright.async_api import Page
import logging

from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageRuntimeState
from core.request.browser.typing import BrowserInteractionPhase, BrowserPageState


logger=logging.getLogger(__name__)

class PlaywrightBrowserPageInspector(
    BrowserPageInspector,
):

    def __init__(
        self,
        detector_registry:
            BrowserPageStateDetectorRegistry,
        stabilizer:
            BrowserPageStabilizer,
    ) -> None:

        self._detectors = detector_registry
        self._stabilizer = stabilizer

    async def inspect(
        self,
        page: Page,
        phase: BrowserInteractionPhase,        
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageInspection:

        snapshot = (
            await self._stabilizer.stabilize(
                page=page,
                phase=phase,
                runtime_state=runtime_state,
            )
        )

        inspection = (
            await self._detectors.detect(
                page,
                snapshot,
            )
        )

        if inspection is None:
            return BrowserPageInspection(
                state=BrowserPageState.UNKNOWN,
                url=snapshot.url,
                title=snapshot.title,
                reason=(
                    "No page-state detector matched."
                ),
            )

        return inspection