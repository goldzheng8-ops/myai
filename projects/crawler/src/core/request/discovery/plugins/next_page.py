

from core.request.discovery.config import NextPageConfig

from core.request.discovery.url.html.base import HtmlDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.typing import RequestKind

class NextPageDiscovery(
    HtmlDiscoveryPlugin[
        NextPageConfig
    ]
):

    plugin_type = DiscoveryType.NEXT_PAGE

    config_type = NextPageConfig

    request_kind = RequestKind.LIST
    