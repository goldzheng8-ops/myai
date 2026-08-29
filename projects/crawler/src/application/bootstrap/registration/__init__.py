from .discoveries import register_discoveries
from .downloaders import register_downloaders
from .extractors import register_extractors
from .middlewares import (
    register_middleware_dependencies,
    register_middlewares,
)
from .resolvers import register_resolvers
from .spider_components import register_spiders
from .transforms import register_transforms
from .adapters import register_adapters
from .runtimes import register_runtimes
from .extraction_services import register_extraction_services
from .lifecycle import register_lifecycle
from .crawler import register_crawler
from .request_services import register_request_services
from .events import register_events

__all__ = [
    "register_discoveries",
    "register_downloaders",
    "register_extractors",
    "register_middleware_dependencies",
    "register_middlewares",
    "register_resolvers",
    "register_spiders",
    "register_transforms",
    "register_adapters",
    "register_runtimes",
    "register_extraction_services",
    "register_lifecycle",
    "register_crawler",
    "register_request_services",
    "register_events",
]