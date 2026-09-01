
from core.request.discovery.config import PageNumberConfig

from core.request.discovery.url.html.base import HtmlDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.typing import RequestKind

class PageNumberDiscovery(
    HtmlDiscoveryPlugin[
        PageNumberConfig
    ]
):

    plugin_type = DiscoveryType.PAGE_NUMBER

    config_type = PageNumberConfig

    request_kind = RequestKind.LIST