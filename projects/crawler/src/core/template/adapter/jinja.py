# template/adapter/jinja.py

from collections.abc import Mapping
from typing import Any

from jinja2 import Template

from .base import RenderableTemplate


class JinjaRenderableTemplate(
    RenderableTemplate,
):

    def __init__(
        self,
        source: str,
        template: Template,
    ) -> None:

        self._source = source
        self._template = template

    @property
    def source(
        self,
    ) -> str:

        return self._source

    def render(
        self,
        context: Mapping[str, Any],
    ) -> str:

        return self._template.render(
            context,
        )