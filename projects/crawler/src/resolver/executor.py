from typing import Any, Protocol

from models.config.value.base import ValueConfig
from models.runtime.extract.context import ExtractContext


class ResolverExecutor(
    Protocol,
):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
    ) -> Any:
        ...