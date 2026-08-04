from abc import ABC
from typing import Any, ClassVar

from .protocol import PluginProtocol


class Plugin(
    PluginProtocol,
    ABC,
):
    """
    Base class of all plugins.
    """

    type: ClassVar[Any]

    name: ClassVar[str] = ""

    version: ClassVar[str] = "1.0"

    description: ClassVar[str] = ""