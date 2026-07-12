from pydantic import BaseModel, Field


class CrawlRequest(BaseModel):
    url: str = Field(..., description="The target article URL")


class CrawlResponse(BaseModel):
    title: str
    content: str
    url: str
    summary: str
