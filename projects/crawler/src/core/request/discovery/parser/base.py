from abc import ABC, abstractmethod


class FeedParser(ABC):

    @abstractmethod
    def parse(
        self,
        content: str,
    ) -> list[str]:
        """
        Parse XML feed and return discovered URLs.
        """