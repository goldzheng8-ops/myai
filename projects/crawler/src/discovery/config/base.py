from core.models.base import BaseConfig
from discovery.config.enums import DiscoveryType


class DiscoveryConfig(BaseConfig):

    enabled: bool = True
    type: DiscoveryType





