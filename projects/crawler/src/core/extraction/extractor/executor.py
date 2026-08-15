from typing import Any, Protocol

from core.extraction.extractor.config import ExtractConfig
from core.extraction.extractor.context import ExtractContext


class ExtractExecutor(
    Protocol,
):

    async def extract(
        self,
        config: ExtractConfig,
        context: ExtractContext,
    ) -> Any:
        ...