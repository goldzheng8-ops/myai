from typing import Any

from core.provider.model import ProviderRegistration
from core.registry.base import Registry


class ProviderRegistry(
    Registry[
        type[Any],
        ProviderRegistration,
    ],
):
    ...