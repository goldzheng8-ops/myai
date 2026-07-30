from abc import ABC, abstractmethod

from extractor.value.template.adapter.base import RenderableTemplate

class TemplateManager(
    ABC,
):

    @abstractmethod
    def load(
        self,
        source: str,
    ) -> RenderableTemplate:
        ...