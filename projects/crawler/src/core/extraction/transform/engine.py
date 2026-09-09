from typing import Any, cast
from collections.abc import Sequence
from core.extraction.transform.config import TransformConfigUnion
from core.extraction.transform.executor import TransformExecutor


from .registry import TransformRegistry




class TransformEngine(
    TransformExecutor,
):

    def __init__(self, registry: TransformRegistry):
        self._registry = registry

    async def transform(
        self,
        value: Any,
        configs: Sequence[TransformConfigUnion],
    ) -> Any:

        result = value

        for config in configs:
            if result is None:
                return None
            plugin = self._registry.create(config.type)

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