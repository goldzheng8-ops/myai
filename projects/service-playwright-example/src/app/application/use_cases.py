from app.domain.models import CrawledArticle
from app.domain.repositories import ArticleCrawler


class NewsCrawlerService:
    """Application use case that orchestrates article crawling."""

    def __init__(self, crawler: ArticleCrawler) -> None:
        self._crawler = crawler

    def execute(self, url: str) -> CrawledArticle:
        payload = self._crawler.fetch_article(url)
        if isinstance(payload, CrawledArticle):
            article = payload
        else:
            article = CrawledArticle(
                title=str(payload.get("title", "Untitled")),
                content=str(payload.get("content", "")),
                url=str(payload.get("url", url)),
            )
        return article
