


from models.config.discovery.rss import RssConfig
from discovery.parser.rss import RssParser
from discovery.url.feed.base import FeedDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from models.enums.request_kind import RequestKind


class RssDiscovery(
    FeedDiscoveryPlugin[
        RssConfig
    ]
):

    plugin_type = DiscoveryType.RSS

    config_type = RssConfig

    parser_cls  = RssParser

    request_kind = RequestKind.DETAIL