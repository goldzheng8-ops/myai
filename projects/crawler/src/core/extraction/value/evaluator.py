from typing import Any, Protocol, Sequence

from core.extraction.transform.config import TransformConfigUnion
from core.extraction.value.config import ValueConfigUnion
from core.extraction.extractor.context import ExtractContext


class ValueExecutor(Protocol):

    async def resolve(
        self,
        config: ValueConfigUnion,
        context: ExtractContext,
        transforms: Sequence[TransformConfigUnion] = (),
    ) -> Any:
        ...