from abc import ABC, abstractmethod

from core.template.backend.base import TemplateBackend




class TemplateExtension(ABC):

    @abstractmethod
    def install(
        self,
        backend: TemplateBackend,
    ) -> None:
        ...