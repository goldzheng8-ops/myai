

from config.discovery.base import ApiDiscoveryConfig
from config.selector.base import SelectorConfig




class CursorApiConfig(ApiDiscoveryConfig):

    selector: SelectorConfig

