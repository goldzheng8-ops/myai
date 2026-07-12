from dataclasses import dataclass


@dataclass(frozen=True)
class CrawledArticle:
    """Core domain model for a collected article."""

    title: str
    content: str
    url: str

    @property
    def summary(self) -> str:
        return self.content.strip()
