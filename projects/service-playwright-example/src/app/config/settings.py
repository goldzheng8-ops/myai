from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "news-crawler-service"
    app_version: str = "0.1.0"
