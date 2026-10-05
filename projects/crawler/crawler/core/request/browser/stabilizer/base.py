from abc import ABC, abstractmethod
from core.request.browser.snapshot import BrowserPageRuntimeState, BrowserPageSnapshot
from core.request.browser.typing import BrowserInteractionPhase
from playwright.async_api import Page

class BrowserPageStabilizer(ABC):

    @abstractmethod
    async def stabilize(
        self,
        page: Page,
        phase: BrowserInteractionPhase,
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageSnapshot:
        raise NotImplementedError