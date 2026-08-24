from typing import Any

from core.registry import Registry
from core.spider.template.base import TemplateSpider


from .typing import SpiderTemplate


class SpiderRegistry(
    Registry[
        SpiderTemplate,
        type[TemplateSpider[Any]],
    ],
):
    pass