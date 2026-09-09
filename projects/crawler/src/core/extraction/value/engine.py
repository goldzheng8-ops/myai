from typing import Any, Sequence

from core.extraction.transform.config import TransformConfigUnion
from core.extraction.value.config import ValueConfigUnion
from core.extraction.extractor.context import ExtractContext
from core.extraction.transform.executor import TransformExecutor
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
        config: ValueConfigUnion,
        context: ExtractContext,
        transforms: Sequence[TransformConfigUnion] = (),
    ) -> Any:

        value = await self._resolver.resolve(
            config,
            context,
        )

        if transforms:
            value = self._transformer.transform(
                value,
                transforms,
            )

        return value