from sqlalchemy.orm import Session

from app.crud.news import create_news, list_news
from app.services.hackernews import get_latest_news


class NewsService:
    async def fetch_news(self, db: Session):
        payload = await get_latest_news()
        return create_news(db, payload)

    def get_news_list(self, db: Session):
        return list_news(db)


news_service = NewsService()