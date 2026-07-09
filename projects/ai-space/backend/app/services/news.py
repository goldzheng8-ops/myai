from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.crud.news import create_news, list_news
from app.models.news import News
from app.services.hackernews import get_latest_news
from playwright.async_api import async_playwright
from typing import List


class NewsService:
    async def fetch_news(self, db: Session):
        payload = await get_latest_news()
        return create_news(db, payload)

    def get_news_list(self, db: Session):
        return list_news(db)

    async def fetch_news_list(self, db: Session) -> dict:
        """Scrape the front page (first 30 `.titleline a`) and save batch, returning stats."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True,proxy={"server": "socks5://127.0.0.1:1080"})
            page = await browser.new_page()
            await page.goto("https://news.ycombinator.com")

            locator = page.locator(".titleline a")
            count = await locator.count()
            limit = min(30, count)

            items: List[dict] = []
            for i in range(limit):
                handle = locator.nth(i)
                title = (await handle.text_content()) or ""
                url = (await handle.get_attribute("href")) or ""
                if url and not url.startswith("http"):
                    url = f"https://news.ycombinator.com/{url.lstrip('/') }"
                items.append({"title": title.strip(), "url": url, "source": "hackernews"})

            await browser.close()

        return self.save_news_list(db, items)

    def save_news_list(self, db: Session, news_list: List[dict]) -> dict:
        """Batch save a list of news dicts. Returns stats {total, inserted, duplicated}."""
        total = len(news_list)
        if total == 0:
            return {"total": 0, "inserted": 0, "duplicated": 0}

        stmt = insert(News).values([
            {
                "title": n["title"],
                "url": n["url"],
                "source": n["source"]
            }
            for n in news_list
        ])
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["url"]
        )
        result = db.execute(stmt)
        db.commit()
        inserted = result.rowcount if result.rowcount is not None else 0
        inserted = max(0, inserted)  # Ensure non-negative
        duplicated = total - inserted
        return {"total": total, "inserted": inserted, "duplicated": duplicated}


news_service = NewsService()