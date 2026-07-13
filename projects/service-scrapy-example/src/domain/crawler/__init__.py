from .config import CrawlerConfig
from .templates import (
    TemplateApiSpider,
    TemplateBrowserSpider,
    TemplateDetailSpider,
    TemplateListSpider,
    build_template_spider,
)

__all__ = [
    "CrawlerConfig",
    "TemplateListSpider",
    "TemplateDetailSpider",
    "TemplateApiSpider",
    "TemplateBrowserSpider",
    "build_template_spider",
]
