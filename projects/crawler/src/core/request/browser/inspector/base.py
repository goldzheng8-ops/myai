from abc import ABC, abstractmethod

from core.extraction.response.playwright import PlaywrightResponseAdapter
from core.request.browser.typing import BrowserPageState



class BrowserPageInspector(ABC):

    @abstractmethod
    async def inspect(
        self,
        response: PlaywrightResponseAdapter,
    ) -> BrowserPageState:
        raise NotImplementedError

# class BrowserPageInspector(ABC):

#     @abstractmethod
#     async def inspect(
#         self,
#         page: Page,
#     ) -> BrowserPageInspection:
#         raise NotImplementedError