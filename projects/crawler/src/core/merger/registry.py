from typing import Any

from core.merger.base import BaseMerger
from core.registry.registry import Registry

class MergerRegistry(
    Registry[
        type[Any],
        BaseMerger[Any],
    ],
):
    pass