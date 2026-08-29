from contextlib import asynccontextmanager

from application.bootstrap.application import ApplicationBootstrap
from application.bootstrap.factory import ApplicationContainerFactory
from application.config.loader import YamlConfigLoader
from application.config.model import CrawlRequest
from application.crawler.application import CrawlerApplication
from fastapi import Depends, FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):

    application = ApplicationBootstrap(
        config_loader=YamlConfigLoader(),
        container_factory=ApplicationContainerFactory(),
    ).create(
        "config/application.yaml",
    )

    app.state.application = application

    try:
        yield

    finally:
        await application.close()


@app.post("/crawl")
async def crawl(
    request: CrawlRequest,
    application: CrawlerApplication = Depends(
        get_application,
    ),
) -> SpiderResult:

    return await application.run(
        request,
    )