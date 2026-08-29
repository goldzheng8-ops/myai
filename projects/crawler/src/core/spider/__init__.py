from .template import TemplateSpider
from .registry import SpiderRegistry
from .factory import (
    SpiderFactory,
    build_api_spider_factory,
    build_browser_spider_factory,
    build_detail_spider_factory,
    build_list_spider_factory,
)
from .typing import SpiderTemplate

__all__=[
    "TemplateSpider",
    "SpiderRegistry",
    "SpiderFactory",
    "build_api_spider_factory",
    "build_browser_spider_factory",
    "build_detail_spider_factory",
    "build_list_spider_factory",
    "SpiderTemplate",
]
