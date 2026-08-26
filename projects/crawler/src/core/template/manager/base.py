from abc import ABC, abstractmethod

from core.runtime import RuntimeContext
from core.template.adapter.base import RenderableTemplate

class TemplateManager(
    ABC,
):

    @abstractmethod
    def load(
        self,
        source: str,
    ) -> RenderableTemplate:
        ...

    @abstractmethod
    def render(
        self,
        template: str,
        context: RuntimeContext,
    ) -> str:
        ...