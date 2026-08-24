from abc import ABC
from typing import Any, ClassVar

from core.request.downloader.base import LifecycleParticipant

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
    
    type: ClassVar[Any]

    name: ClassVar[str] = ""

    version: ClassVar[str] = "1.0"

    description: ClassVar[str] = ""