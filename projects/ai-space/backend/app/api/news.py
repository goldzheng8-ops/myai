from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.news import create_news
from app.db.session import get_db
from app.schemas.news import NewsResponse
from app.services.hackernews import get_latest_news
from app.services.news import news_service


router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/fetch")
async def fetch_news(db: Session = Depends(get_db)):
    return await news_service.fetch_news_list(db)


@router.get("/list")
async def news_list(db: Session = Depends(get_db)):
    return news_service.get_news_list(db)


@router.get(
    "/latest",
    response_model=NewsResponse
)
async def latest_news(db: Session = Depends(get_db)):
    payload = await get_latest_news()
    return create_news(db, payload)