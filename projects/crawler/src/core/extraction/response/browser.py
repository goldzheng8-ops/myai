from abc import abstractmethod

from core.extraction.response.base import ResponseAdapter

class BrowserResponseAdapter(
    ResponseAdapter,
):
    """
    Abstract adapter for browser-backed responses.

    This class defines browser-specific extraction capabilities
    without depending on any concrete browser automation library.
    """

    @abstractmethod
    async def scroll(
        self,
        *,
        count: int = 1,
        delay: float = 0.5,
    ) -> None:
        """
        Scroll the current browser page.
        """
        raise NotImplementedError
