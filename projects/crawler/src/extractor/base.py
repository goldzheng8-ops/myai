from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar

from enums.extract_type import ExtractType
from core.plugin.base import Plugin
from core.context.extract_context import ExtractContext

from .executor import ExtractExecutor

ConfigT=TypeVar("ConfigT")


class Extractor(

    Plugin,

    Generic[ConfigT],

    ABC,
):

    plugin_type: ClassVar[ExtractType]

    @abstractmethod
    async def extract(
        self,
        config: ConfigT,
        context: ExtractContext,
        executor: ExtractExecutor,
    ):
        ...