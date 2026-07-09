from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsBase(BaseModel):
    title: str
    url: str
    source: str


class NewsCreate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)