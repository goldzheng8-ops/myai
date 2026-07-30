
from abc import ABC
from typing import Any, ClassVar



class Plugin(ABC):

    plugin_type: ClassVar[Any]