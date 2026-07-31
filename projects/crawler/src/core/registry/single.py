from typing import Generic
from collections.abc import Iterable

from .plugin import PluginRegistry


from .types import (
    K,
    P,
)


class SingletonPluginRegistry(
    PluginRegistry[K, P],
    Generic[K, P],
):
    """
    Creates only one instance.
    """

    def __init__(
        self,
        plugins:Iterable[type[P]]=(),
    ) -> None:

        super().__init__(plugins)

        self._instances: dict[K, P] = {}

    def create(
        self,
        key: K,
    ) -> P:

        instance = self._instances.get(key)

        if instance is not None:
            return instance

        provider = self._providers.get(key)

        if provider is not None:
            instance = provider()

        else:
            instance = self.get(key)()

        self._instances[key] = instance

        return instance

    def clear_instances(
        self,
    ) -> None:

        self._instances.clear()