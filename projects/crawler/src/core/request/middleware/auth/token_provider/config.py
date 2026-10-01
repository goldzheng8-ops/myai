from typing import Literal

from core.typing.config import BaseConfig

class BrowserTokenProviderConfig(BaseConfig):

    storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ]

    key: str