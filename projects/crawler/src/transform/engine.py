from typing import Any

from .registry import TransformRegistry
from .config.base import TransformConfig


from typing import Any, cast

class TransformEngine:

    def __init__(self, registry: TransformRegistry):
        self.registry = registry

    def transform(
        self,
        value: object,
        configs: list[TransformConfig],
    ) -> object:

        result: object = value

        for config in configs:
            plugin = self.registry.get(config.type)

            if isinstance(result, list):
                result = plugin.transform_many(
                    cast(list[Any], result),
                    config,
                )
            else:
                result = plugin.transform_one(
                    result,
                    config,
                )

        return result