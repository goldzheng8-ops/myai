
from models.config.discovery.detail_link import DetailLinkConfig

from discovery.url.html.base import HtmlDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from models.enums.request_kind import RequestKind


class DetailLinkDiscovery(
    HtmlDiscoveryPlugin[
        DetailLinkConfig
    ]
):

    plugin_type = DiscoveryType.DETAIL_LINK

    config_type = DetailLinkConfig

    request_kind = RequestKind.DETAIL