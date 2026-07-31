from typing import Any, Sequence, cast

from config.transform.base import TransformConfig
from extractor.transform.evaluator import TransformExecutor


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
            plugin = self.registry.create(config.type)

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