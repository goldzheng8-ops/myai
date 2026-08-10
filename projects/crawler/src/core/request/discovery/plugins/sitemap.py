

from models.config.discovery.sitemap import SitemapConfig
from core.request.discovery.parser.sitemap import SitemapParser
from core.request.discovery.url.feed.base import FeedDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from core.request.typing import RequestKind


class SitemapDiscovery(
    FeedDiscoveryPlugin[
        SitemapConfig
    ]
):

    plugin_type = DiscoveryType.SITEMAP

    config_type = SitemapConfig

    parser_cls  = SitemapParser

    request_kind = RequestKind.DETAIL