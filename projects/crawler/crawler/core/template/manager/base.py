from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any


from core.template.adapter.base import RenderableTemplate

class TemplateManager(
    ABC,
):

    @abstractmethod
    def load(
        self,
        source: str,
    ) -> RenderableTemplate:
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        template: str,
        context: Mapping[str, Any],
    ) -> str:
        raise NotImplementedError