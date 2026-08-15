from typing import Any, Sequence

from core.extraction.transform.config import TransformConfig
from core.extraction.value.config import ValueConfig
from core.extraction.extractor.context import ExtractContext
from core.extraction.transform.evaluator import TransformExecutor
from core.extraction.value.evaluator import ValueExecutor
from core.extraction.resolver.executor import ResolverExecutor


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