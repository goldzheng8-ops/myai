from ..config import ApiSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryTemplateSpider

class TemplateApiSpider(
    DiscoveryTemplateSpider[ApiSpiderConfig],
):

    plugin_type = SpiderTemplate.API



