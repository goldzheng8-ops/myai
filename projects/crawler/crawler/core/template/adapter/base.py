# template/adapter/base.py

from abc import ABC
from abc import abstractmethod
from collections.abc import Mapping
from typing import Any


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
        context: Mapping[str, Any],
    ) -> str:
        """Render template."""