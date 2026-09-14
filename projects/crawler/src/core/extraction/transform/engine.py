from typing import Any, cast
from collections.abc import Sequence
from core.extraction.transform.config import TransformConfigUnion
from core.extraction.transform.context import TransformContext
from core.extraction.transform.executor import TransformExecutor
from .registry import TransformRegistry


class TransformEngine(
    TransformExecutor,
):

    def __init__(
        self,
        registry: TransformRegistry,
    ) -> None:
        self._registry = registry

    def transform(
        self,
        *,
        value: Any,
        configs: Sequence[TransformConfigUnion],
        context: TransformContext | None = None,
    ) -> Any:

        result = value

        for config in configs:
            if result is None:
                return None

            plugin = self._registry.create(
                config.type,
            )

            if isinstance(result, list):
                result = plugin.transform_many(
                    cast(list[Any], result),
                    config,
                    context,
                )
            else:
                result = plugin.transform_one(
                    result,
                    config,
                    context,
                )

        return result