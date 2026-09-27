from abc import ABC, abstractmethod

from core.request.browser.interaction.model import BrowserAction
from playwright.async_api import Page


class BrowserActionExecutor(ABC):

    @abstractmethod
    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:
        raise NotImplementedError