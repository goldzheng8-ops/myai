from core.request.browser.detector.registry import BrowserPageStateDetectorRegistry
from core.request.browser.inspector.base import BrowserPageInspector
from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshotBuilder
from playwright.async_api import Page


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
    ) -> BrowserPageInspection:

        snapshot = await self._snapshot_builder.build(
            page,
        )

        inspection = await self._detectors.detect(
            page,
            snapshot,
        )

        if inspection is None:
            raise RuntimeError(
                "Browser page state could not be detected.",
            )

        return inspection