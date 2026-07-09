from fastapi import FastAPI

from app.api.routes.browser import router
from app.api.news import router as news_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title=settings.app_name,
    version=settings.version
)


init_db()

app.include_router(router)
app.include_router(news_router)


@app.get("/")
async def root():
    return {
        "message": settings.app_name
    }