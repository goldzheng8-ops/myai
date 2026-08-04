from typing import Any, ClassVar, Protocol


class PluginProtocol(Protocol):

    type: ClassVar[Any]