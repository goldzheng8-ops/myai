from abc import ABC, abstractmethod

from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.snapshot import BrowserPageSnapshot
from playwright.async_api import Page


class BrowserPageStateDetector(ABC):

    priority: int

    @abstractmethod
    async def detect(
        self,
        page: Page,
        snapshot: BrowserPageSnapshot,
    ) -> BrowserPageInspection | None:
        raise NotImplementedError