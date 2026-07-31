from typing import Any, Protocol, Sequence

from config.transform.base import TransformConfig
from config.value.base import ValueConfig
from core.context.extract_context import ExtractContext


class ValueExecutor(Protocol):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
        transforms: Sequence[TransformConfig] = (),
    ) -> Any:
        ...