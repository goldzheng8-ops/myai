from __future__ import annotations
from abc import ABC, abstractmethod


from core.context.runtime_context import ObjectContext



class TemplateRenderer(ABC):

    @abstractmethod
    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:
        ...