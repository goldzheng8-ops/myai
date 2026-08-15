from typing import Any, Sequence, cast

from core.extraction.transform.config import TransformConfig
from core.extraction.transform.evaluator import TransformExecutor


from .registry import TransformRegistry




class TransformEngine(
    TransformExecutor,
):

    def __init__(self, registry: TransformRegistry):
        self.registry = registry

    def transform(
        self,
        value: Any,
        configs: Sequence[TransformConfig],
    ) -> Any:

        result = value

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