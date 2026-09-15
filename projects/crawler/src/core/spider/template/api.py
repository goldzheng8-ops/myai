from ..config import ApiSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryRequestTemplate

class ApiRequestTemplate(
    DiscoveryRequestTemplate[ApiSpiderConfig],
):

    plugin_type = SpiderTemplate.API



