from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from collections.abc import MutableMapping
from collections.abc import Callable
from typing import Any

TemplateCallable = Callable[..., Any]

T = TypeVar("T")


class BackendRegistry(
    Generic[T],
    ABC,
):

    @abstractmethod
    def register(
        self,
        name: str,
        value: T,
    ) -> None:
        ...



class BaseBackendRegistry(
    BackendRegistry[T],
):

    def __init__(
        self,
        registry: MutableMapping[str, T],
    ) -> None:

        self._registry = registry

    def register(
        self,
        name: str,
        value: T,
    ) -> None:

        if name in self._registry:
            raise ValueError(
                f"{name!r} already registered."
            )

        self._registry[name] = value

class FilterRegistry(
    BaseBackendRegistry[TemplateCallable],
):
    pass


class TestRegistry(
    BaseBackendRegistry[TemplateCallable],
):
    pass


class GlobalRegistry(
    BaseBackendRegistry[TemplateCallable],
):
    pass