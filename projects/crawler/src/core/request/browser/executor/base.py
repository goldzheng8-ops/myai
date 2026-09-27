from abc import ABC, abstractmethod

from core.request.browser.interaction.model import BrowserAction
from core.request.browser.typing import BrowserActionType
from playwright.async_api import Page


class BrowserActionExecutor(ABC):

    @abstractmethod
    def supports(
        self,
        action_type: BrowserActionType,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        page: Page,
        action: BrowserAction,
    ) -> None:
        raise NotImplementedError