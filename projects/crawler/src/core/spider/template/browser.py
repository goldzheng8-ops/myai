from ..config import BrowserSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryTemplateSpider

class TemplateBrowserSpider(
    DiscoveryTemplateSpider[BrowserSpiderConfig],
):

    plugin_type = SpiderTemplate.BROWSER

