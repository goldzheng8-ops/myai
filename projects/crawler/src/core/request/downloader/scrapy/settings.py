from typing import Any

from scrapy.settings import Settings


SCRAPY_HTTPX_DOWNLOAD_HANDLER = (
    "scrapy.core.downloader.handlers._httpx."
    "HttpxDownloadHandler"
)


def create_scrapy_settings(
    settings: dict[str, Any] | None = None,
) -> Settings:

    result = Settings()

    result.set(
        "TWISTED_REACTOR_ENABLED",
        False,
        priority="project",
    )

    result.set(
        "DOWNLOAD_HANDLERS",
        {
            "http": SCRAPY_HTTPX_DOWNLOAD_HANDLER,
            "https": SCRAPY_HTTPX_DOWNLOAD_HANDLER,
        },
        priority="project",
    )

    if settings:
        for name, value in settings.items():
            result.set(
                name,
                value,
                priority="project",
            )

    return result