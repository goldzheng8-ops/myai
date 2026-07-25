
from config.discovery.page_number import PageNumberConfig

from discovery.url.html.base import HtmlDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind

class PageNumberDiscovery(
    HtmlDiscoveryPlugin[
        PageNumberConfig
    ]
):

    plugin_type = DiscoveryType.PAGE_NUMBER

    config_type = PageNumberConfig

    request_kind = RequestKind.LIST