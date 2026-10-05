
from typing import Any

from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.factory import DiscoveryFactory
from core.request.discovery.typing import DiscoveryType
from core.registry import Registry


class DiscoveryRegistry(
    Registry[
        DiscoveryType,
        DiscoveryFactory,
    ],
):
    """
    Registry of discovery plugin factories.
    """

    def create(
        self,
        type_: DiscoveryType,
    ) -> DiscoveryPlugin[Any]:

        return self.get(type_)()