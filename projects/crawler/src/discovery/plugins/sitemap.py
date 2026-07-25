

from config.discovery.sitemap import SitemapConfig
from discovery.parser.sitemap import SitemapParser
from discovery.url.feed.base import FeedDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind


class SitemapDiscovery(
    FeedDiscoveryPlugin[
        SitemapConfig
    ]
):

    plugin_type = DiscoveryType.SITEMAP

    config_type = SitemapConfig

    parser_cls  = SitemapParser

    request_kind = RequestKind.DETAIL