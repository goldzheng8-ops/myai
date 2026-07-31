from typing import Any, Sequence

from config.transform.base import TransformConfig
from config.value.base import ValueConfig
from core.context.extract_context import ExtractContext
from extractor.transform.evaluator import TransformExecutor
from extractor.value.evaluator import ValueExecutor
from resolver.executor import ResolverExecutor


class ValueEngine(
    ValueExecutor,
):

    def __init__(
        self,
        resolver: ResolverExecutor,
        transformer: TransformExecutor,
    ) -> None:

        self._resolver = resolver
        self._transformer = transformer

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
        transforms: Sequence[TransformConfig] = (),
    ) -> Any:

        value = await self._resolver.resolve(
            config,
            context,
        )

        if transforms:
            value = await self._transformer.transform(
                value,
                transforms,
            )

        return value