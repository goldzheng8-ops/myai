
from models.config.discovery.page_number import PageNumberConfig

from core.request.discovery.url.html.base import HtmlDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from core.request.typing import RequestKind

class PageNumberDiscovery(
    HtmlDiscoveryPlugin[
        PageNumberConfig
    ]
):

    plugin_type = DiscoveryType.PAGE_NUMBER

    config_type = PageNumberConfig

    request_kind = RequestKind.LIST