from typing import Any

from core.registry.factory import FactoryPluginRegistry
from models.enums.value_type import ValueType
from resolver.base import Resolver


class ResolverRegistry(

    FactoryPluginRegistry[

        ValueType,

        Resolver[Any],

    ],

):
    pass