

from typing import Any

from enums.value_type import ValueType
from extractor.value.base import ValuePlugin
from registry.plugin_registry import PluginRegistry


class ValueRegistry(

    PluginRegistry[
        ValueType,
        ValuePlugin[Any],
    ]

):
    pass