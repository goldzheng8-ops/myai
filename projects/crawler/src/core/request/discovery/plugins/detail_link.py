
from core.request.discovery.config import DetailLinkConfig

from core.request.discovery.url.html.base import HtmlDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.typing import RequestKind


class DetailLinkDiscovery(
    HtmlDiscoveryPlugin[
        DetailLinkConfig
    ]
):

    plugin_type = DiscoveryType.DETAIL_LINK

    config_type = DetailLinkConfig

    request_kind = RequestKind.DETAIL