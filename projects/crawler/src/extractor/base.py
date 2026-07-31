from abc import ABC, abstractmethod
from typing import  Any, Generic, TypeVar


from config.extractor.base import ExtractConfig
from core.context.extract_context import ExtractContext
from core.plugin.base import Plugin


ConfigT=TypeVar("ConfigT")



ConfigT = TypeVar(
    "ConfigT",
    bound=ExtractConfig,
)


class Extractor(
    Plugin,
    ABC,
    Generic[ConfigT],
):

    plugin_type: Any


    @abstractmethod
    async def extract(
        self,
        config: ConfigT,
        context: ExtractContext,
    ) -> Any:
        ...