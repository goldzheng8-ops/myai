from playwright.async_api import Page
import logging

from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageRuntimeState, BrowserPageSnapshotBuilder
from core.request.browser.typing import BrowserPageState
logger=logging.getLogger(__name__)

class PlaywrightBrowserPageInspector(
    BrowserPageInspector,
):

    def __init__(
        self,
        detector_registry:
            BrowserPageStateDetectorRegistry,
        snapshot_builder:
            BrowserPageSnapshotBuilder,
    ) -> None:

        self._detectors = detector_registry
        self._snapshot_builder = snapshot_builder

    async def inspect(
        self,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageInspection:

        snapshot = await self._snapshot_builder.build(
            page,
            runtime_state,
        )
        logger.info(
            "[BrowserSnapshot] "
            "url=%r title=%r "
            "text_length=%d",
            snapshot.url,
            snapshot.title,
            len(snapshot.body_text),
        )
        logger.info(
            "[BrowserSnapshot] text=%r",
            snapshot.body_text[:500],
        )
        inspection = await self._detectors.detect(
            page,
            snapshot,
        )

        if inspection is None:

            return BrowserPageInspection(
                state=BrowserPageState.UNKNOWN,
                url=snapshot.url,
                title=snapshot.title,
                reason="No page-state detector matched.",
            )

        return inspection