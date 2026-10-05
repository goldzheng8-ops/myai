from typing import Any

from core.extraction.resolver.base import Resolver
from core.extraction.value.typing import ValueType
from core.registry import Registry
from core.extraction.resolver.factory import ResolverFactory



class ResolverRegistry(
    Registry[
        ValueType,
        ResolverFactory,
    ],
):
    """
    Registry of resolver factories.
    """

    def create(
        self,
        type_: ValueType,
    ) -> Resolver[Any]:

        return self.get(type_)()