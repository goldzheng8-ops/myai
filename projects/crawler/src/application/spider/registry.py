

from typing import Any, TypeAlias

from core.registry import Registry
from core.spider.template.base import TemplateSpider



SpiderRegistry: TypeAlias = Registry[
    str,
    type[TemplateSpider[Any]],
]