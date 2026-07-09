from fastapi import APIRouter

from app.services.browser_service import fetch_news


router = APIRouter(
    prefix="/browser"
)


@router.get("/news")
async def news():

    title = await fetch_news()

    return {
        "title":title
    }