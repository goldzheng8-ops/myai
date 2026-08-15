


from core.request.discovery.config import RssConfig
from core.request.discovery.parser.rss import RssParser
from core.request.discovery.url.feed.base import FeedDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.typing import RequestKind


class RssDiscovery(
    FeedDiscoveryPlugin[
        RssConfig
    ]
):

    type = DiscoveryType.RSS

    config_type = RssConfig

    parser_cls  = RssParser

    request_kind = RequestKind.DETAIL