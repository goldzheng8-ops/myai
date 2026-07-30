from abc import ABC, abstractmethod

from adapters.base import ResponseAdapter
from config.value.base import ValueConfig

from typing import Any, ClassVar, Generic, TypeVar
from enums.value_type import ValueType
from core.context.runtime_context import ObjectContext
from core.plugin.base import Plugin
from core.context.extract_context import ExtractContext



ConfigT = TypeVar(
    "ConfigT",
    bound=ValueConfig,
)


class ValuePlugin(
    Plugin,
    Generic[ConfigT],
    ABC,
):

    plugin_type: ClassVar[ValueType]

    config_type: ClassVar[type[ValueConfig]]

    @abstractmethod
    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: ConfigT,
    ) -> Any:
        ...