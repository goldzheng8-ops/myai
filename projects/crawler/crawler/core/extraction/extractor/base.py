from abc import abstractmethod
from typing import  Any, Generic, TypeVar


from core.extraction.extractor.config import ExtractConfig
from core.extraction.extractor.context import ExtractContext
from core.plugin.base import Plugin

ExtractorConfigT = TypeVar(
    "ExtractorConfigT",
    bound=ExtractConfig,
)


class Extractor(
    Plugin,
    Generic[ExtractorConfigT],
):

    plugin_type: Any


    @abstractmethod
    async def extract(
        self,
        config: ExtractorConfigT,
        context: ExtractContext,
    ) -> Any:
        ...