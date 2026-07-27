from abc import ABC
from abc import abstractmethod

from extractor.value.template.backend.registry import FilterRegistry, GlobalRegistry, TestRegistry


class TemplateBackend(
    ABC,
):

    @property
    @abstractmethod
    def filters(
        self,
    ) -> FilterRegistry:
        ...

    @property
    @abstractmethod
    def tests(
        self,
    ) -> TestRegistry:
        ...

    @property
    @abstractmethod
    def globals(
        self,
    ) -> GlobalRegistry:
        ...
