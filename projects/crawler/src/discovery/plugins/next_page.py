

from models.config.discovery.next_page import NextPageConfig

from discovery.url.html.base import HtmlDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from models.enums.request_kind import RequestKind

class NextPageDiscovery(
    HtmlDiscoveryPlugin[
        NextPageConfig
    ]
):

    plugin_type = DiscoveryType.NEXT_PAGE

    config_type = NextPageConfig

    request_kind = RequestKind.LIST
    