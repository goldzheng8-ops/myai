from typing import Protocol

from core.extraction.extractor.config import ExtractConfigUnion
from core.extraction.extractor.context import ExtractContext
from core.extraction.extractor.result import ExtractResult


class ExtractExecutor(
    Protocol,
):

    async def extract(
        self,
        config: ExtractConfigUnion,
        context: ExtractContext,
    ) -> ExtractResult:
        ...