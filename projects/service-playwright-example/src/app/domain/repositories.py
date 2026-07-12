from abc import ABC, abstractmethod

from app.domain.models import CrawledArticle


class ArticleCrawler(ABC):
    """Repository interface for fetching article payloads."""

    @abstractmethod
    def fetch_article(self, url: str) -> CrawledArticle | dict[str, str]:
        """Fetch and normalize an article from a remote URL."""
