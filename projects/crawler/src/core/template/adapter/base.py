# template/adapter/base.py

from abc import ABC
from abc import abstractmethod

from core.context.runtime_context import RuntimeContext


class RenderableTemplate(
    ABC,
):

    @property
    @abstractmethod
    def source(
        self,
    ) -> str:
        """Original template source."""

    @abstractmethod
    def render(
        self,
        context: RuntimeContext,
    ) -> str:
        """Render template."""