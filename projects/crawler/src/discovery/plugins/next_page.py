

from config.discovery.next_page import NextPageConfig
from discovery.base import HtmlDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind

class NextPageDiscovery(
    HtmlDiscoveryPlugin[
        NextPageConfig
    ]
):

    type = DiscoveryType.NEXT_PAGE

    config_type = NextPageConfig

    request_kind = RequestKind.LIST
    