from fastapi import FastAPI

from app.api.routes import router
from app.application.use_cases import NewsCrawlerService
from app.config.settings import Settings
from app.infrastructure.playwright_crawler import PlaywrightCrawler


_service: NewsCrawlerService | None = None


def create_app(service: NewsCrawlerService | None = None) -> FastAPI:
    app = FastAPI(title=Settings().app_name, version=Settings().app_version)
    app.include_router(router)
    app.state.service = service or create_default_service()
    return app


def create_default_service() -> NewsCrawlerService:
    return NewsCrawlerService(PlaywrightCrawler())


def get_service_instance() -> NewsCrawlerService:
    global _service
    if _service is None:
        _service = create_default_service()
    return _service


app = create_app()
