
from models.config.discovery.base import FeedDiscoveryConfig
from models.enums.discovery_type import DiscoveryType

class RssConfig(FeedDiscoveryConfig):

    type = DiscoveryType.RSS