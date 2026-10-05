from typing import Any, ClassVar, Protocol


class PluginProtocol(Protocol):

    plugin_type: ClassVar[Any]