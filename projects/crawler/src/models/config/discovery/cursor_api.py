

from models.config.discovery.base import ApiDiscoveryConfig
from models.config.selector.base import SelectorConfig




class CursorApiConfig(ApiDiscoveryConfig):

    selector: SelectorConfig

