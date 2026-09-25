from abc import ABC, abstractmethod

from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.typing import BrowserPageState
from playwright.async_api import Page


class BrowserPageStateDetector(ABC):

    @abstractmethod
    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,      
    ) -> BrowserPageState | None:
        """
        Return a detected state, or None if this detector
        does not recognize the current page.
        """
        raise NotImplementedError