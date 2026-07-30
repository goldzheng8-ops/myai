from typing import Any, Protocol

from config.extractor.base import ExtractConfig
from core.context.extract_context import ExtractContext


class ExtractExecutor(
    Protocol,
):

    async def extract(
        self,
        config: ExtractConfig,
        context: ExtractContext,
    ) -> Any:
        ...