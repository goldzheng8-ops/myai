

from core.request.discovery.config import SitemapConfig
from core.request.discovery.parser.sitemap import SitemapParser
from core.request.discovery.url.feed.base import FeedDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.typing import RequestKind


class SitemapDiscovery(
    FeedDiscoveryPlugin[
        SitemapConfig
    ]
):

    type = DiscoveryType.SITEMAP

    config_type = SitemapConfig

    parser_cls  = SitemapParser

    request_kind = RequestKind.DETAIL