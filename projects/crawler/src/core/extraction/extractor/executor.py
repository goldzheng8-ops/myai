from typing import Any, Protocol

from models.config.extractor.base import ExtractConfig
from models.runtime.extract.context import ExtractContext


class ExtractExecutor(
    Protocol,
):

    async def extract(
        self,
        config: ExtractConfig,
        context: ExtractContext,
    ) -> Any:
        ...