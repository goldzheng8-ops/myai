from typing import Any, Protocol, Sequence

from models.config.transform.base import TransformConfig
from models.config.value.base import ValueConfig
from models.runtime.extract.context import ExtractContext


class ValueExecutor(Protocol):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
        transforms: Sequence[TransformConfig] = (),
    ) -> Any:
        ...