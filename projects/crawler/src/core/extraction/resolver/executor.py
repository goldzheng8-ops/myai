from typing import Any, Protocol

from core.extraction.value.config import ValueConfig
from core.extraction.extractor.context import ExtractContext


class ResolverExecutor(
    Protocol,
):

    async def resolve(
        self,
        config: ValueConfig,
        context: ExtractContext,
    ) -> Any:
        ...