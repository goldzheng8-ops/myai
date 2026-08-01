

from models.config.discovery.base import FeedDiscoveryConfig
from models.enums.discovery_type import DiscoveryType


class SitemapConfig(FeedDiscoveryConfig):

    type = DiscoveryType.SITEMAP