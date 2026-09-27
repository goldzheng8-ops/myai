from abc import ABC, abstractmethod
from playwright.async_api import Page

from core.request.browser.inspector.model import BrowserPageInspection



class BrowserPageInspector(ABC):

    @abstractmethod
    async def inspect(
        self,
        page: Page,
    ) -> BrowserPageInspection:
        raise NotImplementedError

