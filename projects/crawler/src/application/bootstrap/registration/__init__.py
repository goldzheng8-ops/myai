from .adapters import register_adapters
from .crawler import register_crawler
from .discoveries import register_discoveries
from .downloaders import register_downloaders
from .events import register_events
from .extractors import register_extractors
from .lifecycle import register_lifecycle
from .middlewares import (
    register_middleware_dependencies,
    register_middlewares,
    register_proxy_providers,
    register_user_agent_providers,
)
from .request_services import register_request_services
from .resolvers import register_resolvers
from .runtimes import register_runtimes
from .selector import register_selector_registries
from .spider_components import register_spider_components
from .spider_configs import register_spider_configs
from .template import register_template
from .transforms import register_transforms

__all__ = [
    "register_discoveries",
    "register_downloaders",
    "register_extractors",
    "register_proxy_providers",
    "register_user_agent_providers",
    "register_middleware_dependencies",
    "register_middlewares",
    "register_resolvers",
    "register_spider_components",
    "register_transforms",
    "register_adapters",
    "register_runtimes",
    "register_lifecycle",
    "register_crawler",
    "register_request_services",
    "register_events",
    "register_template",
    "register_selector_registries",
    "register_spider_configs",
]