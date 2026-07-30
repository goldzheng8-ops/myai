

from typing import Any

from enums.value_type import ValueType
from extractor.value.base import ValuePlugin
from core.registry.single import SingletonPluginRegistry



class ValueRegistry(
    SingletonPluginRegistry[
        ValueType,
        ValuePlugin[Any],
    ],
):
    pass