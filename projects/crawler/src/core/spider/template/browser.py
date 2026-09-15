from ..config import BrowserSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryRequestTemplate

class BrowserRequestTemplate(
    DiscoveryRequestTemplate[BrowserSpiderConfig],
):

    plugin_type = SpiderTemplate.BROWSER

