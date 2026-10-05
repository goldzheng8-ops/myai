from abc import ABC
from abc import abstractmethod

from core.template.adapter.base import RenderableTemplate


class TemplateCache(
    ABC,
):

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> RenderableTemplate | None:
        ...

    @abstractmethod
    def put(
        self,
        key: str,
        template: RenderableTemplate,
    ) -> None:
        ...

    @abstractmethod
    def clear(
        self,
    ) -> None:
        ...