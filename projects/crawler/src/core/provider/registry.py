from typing import Any

from core.registry.base import Registry

from .typing import ProviderFactory


class ProviderRegistry(
    Registry[
        type[Any],
        ProviderFactory[Any],
    ],
):
    pass