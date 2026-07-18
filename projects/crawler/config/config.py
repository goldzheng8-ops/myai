from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from selector.base import SelectorConfig



class HttpMethod(str, Enum):

    GET = "GET"

    POST = "POST"

    PUT = "PUT"

    DELETE = "DELETE"




class BrowserEngine(str, Enum):

    PLAYWRIGHT = "playwright"

    SELENIUM = "selenium"

    SCRAPY = "scrapy"

class PaginationStrategy(str, Enum):

    NEXT = "next"

    PAGE = "page"

    OFFSET = "offset"

    CURSOR = "cursor"

class OutputFormat(str, Enum):

    JSON = "json"

    CSV = "csv"

    XLSX = "xlsx"

    DATABASE = "database"

    HTTP = "http"

class SpiderTemplate(str,Enum):

    LIST="list"

    DETAIL="detail"

    API="api"

    BROWSER="browser"



class BrowserWaitUntil(str,Enum):
    
    LOAD="load"

    DOMCONTENTLOADED="domcontentloaded"

    NETWORKIDLE="networkidle"




class RequestConfig(BaseModel):
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    cookies: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    method: HttpMethod = HttpMethod.GET
    body: Any = None
    timeout: int = 30
    retry: int = 3
    proxy: str | None = None




class BrowserConfig(BaseModel):

    enabled:bool=False

    engine:BrowserEngine=BrowserEngine.PLAYWRIGHT

    wait_until:BrowserWaitUntil=BrowserWaitUntil.NETWORKIDLE

    timeout:int=30000

    scroll:bool=False

    scroll_times:int=0

    click_actions:list[SelectorConfig]=Field(default_factory=list)

    js_scripts:list[str]=Field(default_factory=list)

class ListConfig(BaseModel):
    selector: SelectorConfig | None = None
    follow_links: bool = False


class DetailConfig(BaseModel):
    enabled: bool = False
    selector: SelectorConfig | None = None
    url_field: str | None = None


class PaginationConfig(BaseModel):

    enabled: bool=False

    strategy: PaginationStrategy = PaginationStrategy.NEXT

    selector: SelectorConfig | None=None

    page_param:str="page"

    start_page:int=1

    max_pages:int=10

    page_size:int|None=None


class ExtractFieldConfig(BaseModel):

    name: str

    selector: SelectorConfig

    required: bool = False

    default: Any = None

    transforms: list[TransformConfig] = Field(default_factory=list)


class PipelineConfig(BaseModel):

    deduplicate:bool=True

    download_images:bool=False

    image_dir:str="images"

    download_files:bool=False

    file_dir:str="downloads"


class OutputConfig(BaseModel):

    format:OutputFormat=OutputFormat.JSON

    callback_url:str|None=None

    encoding:str="utf-8"


class WorkflowConfig(BaseModel):

    task_name:str=""

    description:str=""

    tags:list[str]=Field(default_factory=list)

    cron:str|None=None

    callback_url:str|None=None


class CrawlerConfig(BaseModel):
    template:SpiderTemplate=SpiderTemplate.LIST
    request: RequestConfig
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    list: ListConfig = Field(default_factory=ListConfig)
    detail: DetailConfig = Field(default_factory=DetailConfig)
    pagination: PaginationConfig = Field(default_factory=PaginationConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrawlerConfig":
        return cls.model_validate(data)
