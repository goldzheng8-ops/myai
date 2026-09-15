from ..config import ListSpiderConfig


from ..typing import SpiderTemplate
from .base import DiscoveryRequestTemplate


class ListRequestTemplate(
    DiscoveryRequestTemplate[ListSpiderConfig],
):

    plugin_type = SpiderTemplate.LIST

