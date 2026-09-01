
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from core.plugin.base import Plugin
from core.extraction.extractor.context import ExtractContext

ConfigT = TypeVar(
    "ConfigT",
)
class Resolver(

    Plugin,

    Generic[ConfigT],

    ABC,

):

    @abstractmethod
    async def resolve(

        self,

        config: ConfigT,

        context: ExtractContext,

    ) -> Any:
        ...