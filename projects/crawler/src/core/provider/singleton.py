from typing import Any, Mapping

from .factory import FactoryProvider
from .typing import T
from .manager import ProviderManager
from .registry import ProviderRegistry

class SingletonProvider(
    FactoryProvider,
):

    def __init__(
        self,
        registry: ProviderRegistry,
        manager: ProviderManager,
    ) -> None:

        super().__init__(
            registry,
            manager,
        )

        self._instances: dict[
            type[Any],
            Any,
        ] = {}

    def get(
        self,
        service: type[T],
    ) -> T:

        instance = self._instances.get(
            service,
        )

        if instance is None:

            instance = self._create(
                service,
            )

            self._instances[
                service
            ] = instance

        return instance

    @property
    def instances(
        self,
    ) -> Mapping[type[Any], Any]:
        return self._instances