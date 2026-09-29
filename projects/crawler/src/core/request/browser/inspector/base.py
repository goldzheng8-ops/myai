from abc import ABC, abstractmethod
from core.request.browser.snapshot import BrowserPageRuntimeState
from playwright.async_api import Page

from core.request.browser.inspector.model import BrowserPageInspection



class BrowserPageInspector(ABC):

    @abstractmethod
    async def inspect(
        self,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageInspection:
        raise NotImplementedError

