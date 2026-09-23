from abc import ABC, abstractmethod
from typing import Any

from core.request.browser.interaction.context import BrowserInteractionContext


class BrowserInteractionEngine(ABC):

    @abstractmethod
    async def execute(
        self,
        context: BrowserInteractionContext[Any],
    ) -> None:
        raise NotImplementedError
