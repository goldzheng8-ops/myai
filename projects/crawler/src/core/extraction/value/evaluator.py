from typing import Any, Protocol, Sequence

from core.extraction.transform.config import TransformConfig
from core.extraction.value.config import ValueConfig
from core.extraction.extractor.context import ExtractContext


class ValueExecutor(Protocol):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
        transforms: Sequence[TransformConfig] = (),
    ) -> Any:
        ...