from core.models.base import BaseConfig
from enums.discovery_type import DiscoveryType


class DiscoveryConfig(BaseConfig):

    enabled: bool = True
    type: DiscoveryType





