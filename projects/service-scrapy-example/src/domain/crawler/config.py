from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RequestConfig(BaseModel):
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    cookies: dict[str, str] = Field(default_factory=dict)
    method: str = "GET"
    timeout: int = 30


class BrowserConfig(BaseModel):
    enabled: bool = False
    wait_for: str | None = None
    scroll: bool = False
    click: list[str] = Field(default_factory=list)


class ListConfig(BaseModel):
    selector: str | None = None
    follow_links: bool = False


class DetailConfig(BaseModel):
    enabled: bool = False
    selector: str | None = None
    url_field: str | None = None


class PaginationConfig(BaseModel):
    enabled: bool = False
    next_page_selector: str | None = None
    start_page: int = 1
    max_pages: int = 3


class ExtractFieldConfig(BaseModel):
    selector: str | None = None
    type: str = "text"
    attribute: str | None = None
    default: Any = None


class ExtractConfig(BaseModel):
    fields: dict[str, ExtractFieldConfig] = Field(default_factory=dict)


class PipelineConfig(BaseModel):
    deduplicate: bool = False
    download_images: bool = False
    download_files: bool = False


class OutputConfig(BaseModel):
    format: str = "json"
    callback_url: str | None = None


class WorkflowConfig(BaseModel):
    task_name: str | None = None
    schedule: str | None = None
    ai_space_callback: str | None = None


class CrawlerConfig(BaseModel):
    template: str = "list"
    request: RequestConfig
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    list: ListConfig = Field(default_factory=ListConfig)
    detail: DetailConfig = Field(default_factory=DetailConfig)
    pagination: PaginationConfig = Field(default_factory=PaginationConfig)
    extract: ExtractConfig = Field(default_factory=ExtractConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrawlerConfig":
        return cls.model_validate(data)
