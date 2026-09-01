from typing import Any, Protocol

from core.extraction.extractor.config import ExtractConfigUnion
from core.extraction.extractor.context import ExtractContext


class ExtractExecutor(
    Protocol,
):

    async def extract(
        self,
        config: ExtractConfigUnion,
        context: ExtractContext,
    ) -> Any:
        ...