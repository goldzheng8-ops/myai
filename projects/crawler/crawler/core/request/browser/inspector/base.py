from abc import ABC, abstractmethod
from core.request.browser.snapshot import BrowserPageRuntimeState
from core.request.browser.typing import BrowserInteractionPhase
from playwright.async_api import Page

from core.request.browser.inspector.model import BrowserPageInspection



class BrowserPageInspector(ABC):

    @abstractmethod
    async def inspect(
        self,
        page: Page,
        phase: BrowserInteractionPhase,  
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageInspection:
        raise NotImplementedError

