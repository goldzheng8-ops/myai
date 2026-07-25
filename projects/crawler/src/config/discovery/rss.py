
from config.discovery.base import FeedDiscoveryConfig
from enums.discovery_type import DiscoveryType

class RssConfig(FeedDiscoveryConfig):

    type = DiscoveryType.RSS