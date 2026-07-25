

from config.discovery.base import FeedDiscoveryConfig
from enums.discovery_type import DiscoveryType


class SitemapConfig(FeedDiscoveryConfig):

    type = DiscoveryType.SITEMAP