
from config.discovery.page_number import PageNumberConfig
from discovery.base import HtmlDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind

class PageNumberDiscovery(
    HtmlDiscoveryPlugin[
        PageNumberConfig
    ]
):

    type = DiscoveryType.PAGE_NUMBER

    config_type = PageNumberConfig

    request_kind = RequestKind.LIST