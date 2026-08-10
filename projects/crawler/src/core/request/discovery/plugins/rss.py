


from models.config.discovery.rss import RssConfig
from core.request.discovery.parser.rss import RssParser
from core.request.discovery.url.feed.base import FeedDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from core.request.typing import RequestKind


class RssDiscovery(
    FeedDiscoveryPlugin[
        RssConfig
    ]
):

    plugin_type = DiscoveryType.RSS

    config_type = RssConfig

    parser_cls  = RssParser

    request_kind = RequestKind.DETAIL