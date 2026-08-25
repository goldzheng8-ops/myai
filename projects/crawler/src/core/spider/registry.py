from typing import Any

from core.registry import Registry
from core.spider.factory import SpiderFactory
from core.spider.template.base import TemplateSpider


from .typing import SpiderTemplate


class SpiderRegistry(
    Registry[
        SpiderTemplate,
        SpiderFactory,
    ],
):
    """
    Registry of spider factories.
    """

    def create(
        self,
        template: SpiderTemplate,
    ) -> TemplateSpider[Any]:

        return self.get(template)()