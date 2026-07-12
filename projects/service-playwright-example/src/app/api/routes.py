from fastapi import APIRouter, Depends, Request

from app.application.use_cases import NewsCrawlerService
from app.schemas.news import CrawlRequest, CrawlResponse

router = APIRouter()


def get_service(request: Request) -> NewsCrawlerService:
    return request.app.state.service


@router.post("/news/crawl", response_model=CrawlResponse)
def crawl_news(payload: CrawlRequest, service: NewsCrawlerService = Depends(get_service)) -> CrawlResponse:
    article = service.execute(payload.url)
    return CrawlResponse(
        title=article.title,
        content=article.content,
        url=article.url,
        summary=article.summary,
    )
