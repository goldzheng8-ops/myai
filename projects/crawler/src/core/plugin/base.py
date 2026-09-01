from abc import ABC
from typing import Any, ClassVar

from core.lifecycle.protocol import LifecycleParticipant

from .protocol import PluginProtocol


class Plugin(
    LifecycleParticipant,
    PluginProtocol,
    ABC,
):
    """
    Base class of all plugins.
    """
    async def start(
        self,
    ) -> None:

        return None

    async def close(
        self,
    ) -> None:

        return None
    
    plugin_type: ClassVar[Any]

    name: ClassVar[str] = ""

    version: ClassVar[str] = "1.0"

    description: ClassVar[str] = ""