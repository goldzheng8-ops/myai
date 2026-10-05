from typing import Any
from core.cache.plugin import CachePlugin
from core.registry.base import Registry
class CacheRegistry(
    Registry[
        str,
        type[CachePlugin[Any, Any]],
    ],
):
    pass

