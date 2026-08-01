from abc import ABC
from abc import abstractmethod
from typing import ClassVar

from models.enums.template_backend import TemplateBackendType
from core.template.backend.registry import FilterRegistry, GlobalRegistry, TestRegistry
from core.template.adapter.base import RenderableTemplate
from core.plugin.base import Plugin

class TemplateBackend(
    Plugin,
    ABC,
):
    plugin_type: ClassVar[TemplateBackendType]

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

    @abstractmethod
    def compile(
        self,
        source: str,
    ) -> RenderableTemplate:
        ...
