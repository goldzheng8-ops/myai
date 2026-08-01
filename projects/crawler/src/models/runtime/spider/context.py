from dataclasses import dataclass, field
from typing import Any

from models.config.spider import SpiderConfig

@dataclass(slots=True)
class SpiderContext:

    config: SpiderConfig

    state: dict[str, Any] = field(default_factory=dict)

    stats: dict[str, Any] = field(default_factory=dict)

    cache: dict[str, Any] = field(default_factory=dict)

    session: dict[str, Any] = field(default_factory=dict)