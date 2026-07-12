from __future__ import annotations

from playwright.sync_api import sync_playwright

from app.domain.models import CrawledArticle
from app.domain.repositories import ArticleCrawler


class PlaywrightCrawler(ArticleCrawler):
    """Infrastructure adapter that uses Playwright to read a page."""

    def fetch_article(self, url: str) -> CrawledArticle:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            title = page.title()
            content = page.locator("body").inner_text()
            browser.close()

        return CrawledArticle(title=title, content=content, url=url)
