
from config.discovery.detail_link import DetailLinkConfig
from discovery.base import HtmlDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind


class DetailLinkDiscovery(
    HtmlDiscoveryPlugin[
        DetailLinkConfig
    ]
):

    type = DiscoveryType.DETAIL_LINK

    config_type = DetailLinkConfig

    request_kind = RequestKind.DETAIL