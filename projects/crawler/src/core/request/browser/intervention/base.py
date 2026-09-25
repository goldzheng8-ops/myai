from abc import ABC, abstractmethod
from typing import Any

from core.request.browser.interaction.context import BrowserInteractionContext


class HumanInterventionEngine(ABC):

    @abstractmethod
    async def intervene(
        self,
        context: BrowserInteractionContext[Any],
    ) -> None:
        raise NotImplementedError

# class HumanInterventionEngine(ABC):

#     @abstractmethod
#     async def intervene(
#         self,
#         context: BrowserInteractionContext[Any],
#         inspection: BrowserPageInspection,
#     ) -> None:
#         raise NotImplementedError