from __future__ import annotations

import scrapy
from scrapy.http import Response

from .config import CrawlerConfig


class TemplateListSpider(scrapy.Spider):
    name = "TemplateListSpider"
    custom_settings = {"LOG_LEVEL": "INFO"}

    def __init__(self, *args, crawler_config: CrawlerConfig | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawler_config = crawler_config
        self.start_urls = [crawler_config.request.url] if crawler_config else []

    def parse(self, response: Response, **kwargs):
        selector = self.crawler_config.list.selector if self.crawler_config else None
        if selector:
            for item in response.css(selector):
                yield {
                    "url": response.url,
                    "selector": selector,
                    "content": item.get() or "",
                }
        else:
            yield {"url": response.url, "content": response.text}


class TemplateDetailSpider(TemplateListSpider):
    name = "TemplateDetailSpider"


class TemplateApiSpider(TemplateListSpider):
    name = "TemplateApiSpider"


class TemplateBrowserSpider(TemplateListSpider):
    name = "TemplateBrowserSpider"


def build_template_spider(config: CrawlerConfig, task_id: str) -> type[scrapy.Spider]:
    class DynamicTemplateSpider(TemplateListSpider):
        name = f"TemplateListSpider-{task_id}"

    DynamicTemplateSpider.crawler_config = config
    DynamicTemplateSpider.start_urls = [config.request.url]
    return DynamicTemplateSpider
