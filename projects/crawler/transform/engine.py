from typing import Any

from .registry import TransformRegistry
from .config.base import TransformConfig


class TransformEngine:

    def __init__(self, registry: TransformRegistry):
        self.registry = registry

    def transform(
        self,
        value: Any,
        configs: list[TransformConfig],
    ) -> Any:

        result = value

        for config in configs:
            plugin = self.registry.get(config.type)
            result = plugin.transform(result, config)

        return result