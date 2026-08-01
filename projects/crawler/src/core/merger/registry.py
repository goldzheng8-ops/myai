from typing import Any

from core.merger.base import BaseMerger
from core.registry.single import SingletonPluginRegistry

class MergerRegistry(
    SingletonPluginRegistry[
        type[Any],
        BaseMerger[Any],
    ],
):
    pass