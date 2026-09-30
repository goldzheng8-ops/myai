from core.request.browser.runtime_debugger import BrowserRuntimeDebugger
from core.request.browser.stabilizer.base import BrowserPageStabilizer
from playwright.async_api import Page


from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageRuntimeState
from core.request.browser.typing import BrowserInteractionPhase, BrowserPageState



class PlaywrightBrowserPageInspector(
    BrowserPageInspector,
):

    def __init__(
        self,
        detector_registry: BrowserPageStateDetectorRegistry,
        stabilizer: BrowserPageStabilizer,
        debugger: BrowserRuntimeDebugger,
    ) -> None:
        self._detectors = detector_registry
        self._stabilizer = stabilizer
        self._debugger = debugger

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
        self._debugger.log_detector(
            phase=phase,
            snapshot=snapshot,
            inspection=inspection,
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