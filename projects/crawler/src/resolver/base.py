
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from config.value.base import ValueConfig
from core.plugin.base import Plugin
from core.context.extract_context import ExtractContext

ConfigT = TypeVar(
    "ConfigT",
    bound=ValueConfig,
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