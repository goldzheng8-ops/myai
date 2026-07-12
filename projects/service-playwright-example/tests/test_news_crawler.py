from fastapi.testclient import TestClient

from app.main import create_app
from app.application.use_cases import NewsCrawlerService


class DummyCrawlerGateway:
    def fetch_article(self, url: str) -> dict[str, str]:
        return {
            "title": "Example News",
            "content": "Playwright-powered crawler service returns structured content.",
            "url": url,
        }


def test_use_case_builds_summary_from_article_content():
    service = NewsCrawlerService(DummyCrawlerGateway())

    result = service.execute("https://example.com/news")

    assert result.title == "Example News"
    assert result.url == "https://example.com/news"
    assert result.summary == "Playwright-powered crawler service returns structured content."


def test_crawl_endpoint_returns_structured_payload():
    app = create_app(service=NewsCrawlerService(DummyCrawlerGateway()))
    client = TestClient(app)

    response = client.post("/news/crawl", json={"url": "https://example.com/news"})

    assert response.status_code == 200
    assert response.json()["title"] == "Example News"
    assert response.json()["summary"] == "Playwright-powered crawler service returns structured content."
