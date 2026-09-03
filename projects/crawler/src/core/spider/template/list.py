from ..config import ListSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryTemplateSpider


class TemplateListSpider(
    DiscoveryTemplateSpider[ListSpiderConfig],
):

    plugin_type = SpiderTemplate.LIST

