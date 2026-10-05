from abc import ABC, abstractmethod
from typing import Any

from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.interaction.context import BrowserInteractionContext


class HumanInterventionHandler(ABC):

    @abstractmethod
    async def wait_for_intervention(
        self,
        context: BrowserInteractionContext[Any],
        inspection: BrowserPageInspection,
    ) -> None:
        raise NotImplementedError