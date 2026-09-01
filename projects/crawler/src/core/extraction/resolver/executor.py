from typing import Any, Protocol

from core.extraction.value.config import ValueConfigUnion
from core.extraction.extractor.context import ExtractContext


class ResolverExecutor(
    Protocol,
):

    async def resolve(
        self,
        config: ValueConfigUnion,
        context: ExtractContext,
    ) -> Any:
        ...