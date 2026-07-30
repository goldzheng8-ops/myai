from typing import Any, Protocol

from config.value.base import ValueConfig
from core.context.extract_context import ExtractContext


class ResolverExecutor(
    Protocol,
):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
    ) -> Any:
        ...